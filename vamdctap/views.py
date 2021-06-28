# -*- coding: utf-8 -*-
from django.shortcuts import render,get_object_or_404
from django.template import loader
from django.http import HttpResponseRedirect, HttpResponse, StreamingHttpResponse, FileResponse
from django.shortcuts import redirect

import datetime
import uuid
from io import StringIO
import os, math, sys
from base64 import b64encode
randStr = lambda n: b64encode(os.urandom(int(math.ceil(0.75*n))))[:n]
import time

import logging
log=logging.getLogger('vamdc.tap')

from django.conf import settings
from importlib import import_module
from django.utils.http import http_date
from django.utils import timezone
from requests.utils import CaseInsensitiveDict as CaselessDict

import sqlite3

import threading

from vamdctap.asynchronous import asyncTapQuery
from vamdctap.models import Job


if settings.QUERY_STORE_ACTIVE:
    try:
        import requests as librequests
    except:
        log.critical('settings.QUERY_STORE_ACTIVE is True but requests package is missing!')

QUERYFUNC = import_module(settings.NODEPKG+'.queryfunc')
DICTS = import_module(settings.NODEPKG+'.dictionaries')

# import helper modules that reside in the same directory
NODEID = CaselessDict(DICTS.RETURNABLES)['NodeID']
from .generators import *
from .sqlparse import SQL

REQUESTABLES = [req.lower() for req in [\
 'AtomStates',
 'Atoms',
 'Collisions',
 'Environments',
 'Functions',
 'Methods',
 'MoleculeBasisStates',
 'MoleculeQuantumNumbers',
 'MoleculeStates',
 'Molecules',
 'NonRadiativeTransitions',
 'Particles',
 'Processes',
 'RadiativeCrossSections',
 'RadiativeTransitions',
 'Solids',
 'Sources',
 'Species',
 'States'] ]


# This turns a 404 "not found" error into a TAP error-document
def tapNotFoundError(request, exception):
    text = 'Resource not found: %s'%request.path;
    document = loader.get_template('tap/TAP-error-document.xml').render({"error_message_text" : text})
    return HttpResponse(document, status=404, content_type='text/xml');

# This turns a 500 "internal server error" into a TAP error-document
def tapServerError(request=None, status=500, errmsg=''):
    text = 'Error in TAP service: %s'%errmsg
    document = loader.get_template('tap/TAP-error-document.xml').render({"error_message_text" : text})
    return HttpResponse(document, status=status, content_type='text/xml');

def getBaseURL(request):
    return getattr(settings, 'DEPLOY_URL', None) or \
        'http://' + request.get_host() + request.path.split('/tap',1)[0] + '/tap/'

def getFormatLastModified(lastmodified):
    return http_date(time.mktime(lastmodified.timetuple()))


class TAPQUERY(object):
    """
    This class holds the query, does some validation
    and triggers the SQL parser.
    """
    def __init__(self,request):
        if 'X_REQUEST_METHOD' in request.META: # workaround for mod_wsgi
            self.XRequestMethod = request.META['X_REQUEST_METHOD']
        self.HTTPmethod = request.method
        self.isvalid = True
        self.errormsg = ''
        self.token = request.token
        try:
            self.request=CaselessDict(dict(request.GET or request.POST))
        except Exception as e:
            self.isvalid = False
            self.errormsg = 'Could not read argument dict: %s'%e
            log.error(self.errormsg)

        if self.isvalid:
            self.validate()

        self.fullurl = getBaseURL(request) + 'sync?' + request.META.get('QUERY_STRING')

    def validate(self):
        try:
            self.lang = self.request['LANG'][0]
            self.lang = self.lang.lower()
            log.info(self.lang)
        except:
            log.debug('LANG is empty, assuming VSS2')
            self.lang='vss2'
        else:
            if self.lang not in ('vss1','vss2'):
                self.errormsg += 'Only LANG=VSS1 or LANG=VSS2 is supported.\n'

        try: 
            self.query = self.request['QUERY'][0]
        except: 
            self.errormsg += 'Cannot find QUERY in request.\n'

        try:
            self.format = self.request['FORMAT'][0]
            self.format = self.format.lower()
        except:
            log.debug('FORMAT is empty, assuming XSAMS')
            self.format='xsams'
        else:
            if self.format != 'xsams':
                log.debug('Requested FORMAT is not XSAMS, letting it pass anyway.')
        try: self.parsedSQL=SQL.parseString(self.query,parseAll=True)
        except: # if this fails, we're done
            self.errormsg += 'Could not parse the SQL query string: %s\n'%getattr(self,'query',None)
            self.isvalid=False
            return

        self.requestables = set()
        self.where = self.parsedSQL.where
        if self.parsedSQL.columns[0] not in ('*', 'ALL'):
            for r in self.parsedSQL.columns[0]:
                r = r.lower()
                if r not in REQUESTABLES:
                    self.errormsg += 'Unknown Requestable: %s\n' % r
                else:
                    self.requestables.add(r)

            if 'species' in self.requestables:
                self.requestables.add('atoms')
                self.requestables.add('molecules')
                self.requestables.add('particles')
                self.requestables.add('solids')
            if 'states' in self.requestables:
                self.requestables.add('atomstates')
                self.requestables.add('moleculestates')
            if 'atomstates' in self.requestables:
                self.requestables.add('atoms')
            if 'moleculestates' in self.requestables:
                self.requestables.add('molecules')
            if 'moleculequantumnumbers' in self.requestables:
                self.requestables.add('molecules')
                self.requestables.add('moleculestates')
            if 'moleculebasisstates' in self.requestables:
                self.requestables.add('molecules')
                self.requestables.add('moleculestates')
            if 'processes' in self.requestables:
                self.requestables.add('radiativetransitions')
                self.requestables.add('nonradiativetransitions')
                self.requestables.add('collisions')
            # Always return sources, methods, functions for now.
            self.requestables.add('sources')
            self.requestables.add('functions')
            self.requestables.add('methods')

        if self.errormsg:
            self.isvalid=False

    def __str__(self):
        return '%s'%self.query

def addHeaders(headers,request,response):
    HEADS=['COUNT-SOURCES',
           'COUNT-ATOMS',
           'COUNT-MOLECULES',
           'COUNT-SPECIES',
           'COUNT-STATES',
           'COUNT-COLLISIONS',
           'COUNT-RADIATIVE',
           'COUNT-NONRADIATIVE',
           'TRUNCATED',
           'APPROX-SIZE',
           'REQUEST-TOKEN']

    headers = CaselessDict(headers)

    headlist_asString=''
    for h in HEADS:
        if h in headers:
            response['VAMDC-'+h] = '%s'%headers[h]
            headlist_asString += 'VAMDC-'+h+', '

    response['Access-Control-Allow-Origin'] = '*'
    response['Access-Control-Expose-Headers'] = headlist_asString[:-2]

    lastmod = headers.get('LAST-MODIFIED')
    if not lastmod and hasattr(settings,'LAST_MODIFIED'):
        lastmod=settings.LAST_MODIFIED

    if isinstance(lastmod,datetime.date):
        response['Last-Modified'] = getFormatLastModified(lastmod)
    elif isinstance(lastmod,str):
        response['Last-Modified'] = lastmod
    else:
        pass

    return response

def CORS_request(request):
    """ Allow cross-server requests http://www.w3.org/TR/cors/ """
    log.info('CORS-Request from %s'%(request.META['REMOTE_ADDR']))
    response = HttpResponse('', status=200)
    response['Access-Control-Allow-Origin'] = '*'
    response['Access-Control-Allow-Methods'] = 'HEAD'
    response['Access-Control-Allow-Headers'] = 'VAMDC'

    return response

# Decorator for sync() for logging to the central service
def logCentral(sync):
    def wrapper(request, *args, **kwargs):
        response = sync(request, *args, **kwargs)
        taprequest = TAPQUERY(request)
        #log the request in the query store
        #if the request comes from the query store it is ignored
        user_agent = request.META.get('HTTP_USER_AGENT')
        if request.method in ['GET', 'HEAD'] and \
           response.status_code == 200 and \
           user_agent not in (settings.QUERY_STORE_USER_AGENT, None) and \
           settings.QUERY_STORE_ACTIVE:
            logdata = {
                        # request unique ID
                       'secret': 'vamdcQS',
                       'queryToken': request.token,
                       'accededResource': getBaseURL(request),
                       'resourceVersion': settings.NODEVERSION,
                       'userEmail': '',   # not used in this context
                       'usedClient': user_agent,
                       'accessType': request.method,   # HEAD or GET
                       'outputFormatVersion': settings.VAMDC_STDS_VERSION,
                       'dataURL': "%ssync?%s"%(getBaseURL(request), request.META['QUERY_STRING']),
                       'query' :  taprequest
                       }

            try:
                # SEND THE ACTUAL REQUEST
                logreq = librequests.post(settings.QUERY_STORE_URL,
                    params=logdata, timeout=2000)
            except Exception as e:
                log.warn('Query Store unreachable! %s'%e)
            else:
                if logreq.status_code != 200:
                  log.warn('Query Store returned code: %s' % logreq.status_code)
                  log.debug('QS reply text:\n%s' % logreq.text)
        return response
    return wrapper


@logCentral
def sync(request):

    request.token = "%s:%s:%s" % (settings.NODENAME, uuid.uuid4(), request.method.lower())

    if request.method=='OPTIONS':
        return CORS_request(request)

    log.info('Request from %s: %s'%(request.META['REMOTE_ADDR'], request.GET or request.POST))
    tap=TAPQUERY(request)
    if not tap.isvalid:
        emsg = 'TAP-Request invalid: %s'%tap.errormsg
        log.error(emsg)
        return tapServerError(status=400,errmsg=emsg)

    # if the requested format is not XSAMS, hand over to the node QUERYFUNC
    if tap.format != 'xsams' and tap.format != 'sqlite' and hasattr(QUERYFUNC,'returnResults'):
        log.debug("using custom QUERYFUNC.returnResults(tap)")
        return QUERYFUNC.returnResults(tap)

    # otherwise, setup the results and build the XSAMS response here
    try: querysets = QUERYFUNC.setupResults(tap)
    except Exception as err:
        emsg = 'Query processing in setupResults() failed: %s'%err
        log.debug(emsg)
        return tapServerError(status=400,errmsg=emsg)

    if not querysets:
        log.info('setupResults() gave something empty. Returning 204.')
        response=HttpResponse('', status=204)
        response['Access-Control-Allow-Origin'] = '*'
        return response

    log.debug('Requestables: %s'%tap.requestables)

    if tap.format == 'xsams':
        if hasattr(QUERYFUNC,'customXsams'):
            log.debug("using QUERYFUNC.customXsams as generator")
            generator = QUERYFUNC.customXsams(tap=tap,**querysets)
        else:
            generator = Xsams(tap=tap,**querysets)

        log.debug('Generator set up, handing it to HttpResponse.')
        response=StreamingHttpResponse(generator,content_type='text/xml')
        response['Content-Disposition'] = 'attachment; filename=%s-%s.%s'%(NODEID,
            datetime.datetime.now().isoformat(), tap.format)

        headers = querysets.get('HeaderInfo') or {}
        headers["REQUEST-TOKEN"] = request.token

        response=addHeaders(headers,request,response)
        # Override with empty response if result is empty
        if 'VAMDC-APPROX-SIZE' in response:
            try:
                size = float(response['VAMDC-APPROX-SIZE'])
                if size == 0.0:
                    log.info('Empty result')
                    response.status_code=204
                    return response
            except: pass

        return response

    elif tap.format == 'sqlite':
    
        # Pick a unique ID for this request.
        id = uuid.uuid4()
        
        # Form a unique file-name for the results.
        filePath = settings.RESULTS_CACHE_DIR + os.path.sep + str(id)
        fileName = 'vamdc-tap-result.sqlite3'
        
        # Run the query and put the results into the file.
        generateSqlite(filePath, tap, **querysets)
        
        # Stream the file to the client.
        # Adapted from https://stackoverflow.com/questions/1156246/having-django-serve-downloadable-files
        response = FileResponse(open(filePath, 'rb'), content_type="application/x-sqlite3")
        response['Content-Disposition'] = 'attachment; filename="%s"'%fileName
        return response


def asynch(request):

    request.token = "%s:%s:%s" % (settings.NODENAME, uuid.uuid4(), request.method.lower())

    if request.method=='OPTIONS':
        return CORS_request(request)

    log.info('Request from %s: %s'%(request.META['REMOTE_ADDR'], request.GET or request.POST))
    tap=TAPQUERY(request)
    if not tap.isvalid:
        emsg = 'TAP-Request invalid: %s'%tap.errormsg
        log.error(emsg)
        return tapServerError(status=400,errmsg=emsg)

    # Submit the query for asynchronous execution
    id = uuid.uuid4()
    expiry = timezone.now()
    expiry += datetime.timedelta(days=1)
    j = Job()
    j.id = str(id)
    j.query = tap.query
    j.phase = 'pending'
    j.expiry = expiry
    j.file = j.id + '.sqlite3'
    j.save()
    dir = settings.RESULTS_CACHE_DIR
    thread = threading.Thread(target=asyncTapQuery, args=(str(id), tap, dir,))
    thread.start()
    
    # Redirect to job page
    job_url = '/tap/async/jobs/' + str(id)
    return redirect(job_url)
    
    
        
def generateSqlite(filePath, tap, HeaderInfo=None, Sources=None, Methods=None, Functions=None,
          Environments=None, Atoms=None, Molecules=None, Solids=None, Particles=None,
          CollTrans=None, RadTrans=None, RadCross=None, NonRadTrans=None):
          
    try:
        log.debug('Connecting SQLite to %s...'%filePath)
        conn = sqlite3.connect(filePath)
        log.debug('...connected')
        c = conn.cursor()
        ATOMS_CREATE = '''CREATE TABLE Atoms(
            AtomSpeciesId INTEGER PRIMARY KEY,
            AtomSymbol CHAR(2),
            AtomNuclearCharge INTEGER,
            AtomIonCharge INTEGER,
            AtomInchi VARCHAR(64),
            AtomInchiKey VARCHAR(32))'''
        c.execute(ATOMS_CREATE)
        ATOMSTATE_CREATE = '''CREATE TABLE AtomicStates(
            AtomStateId INTEGER PRIMARY KEY, 
            AtomRef INTEGER REFERENCES Atoms(AtomSpeciesId),
            AtomStateTotalAngMom FLOAT, 
            AtomStateParity INTEGER, 
            AtomStateStatisticalWeight FLOAT,
            AtomStateEnergy DOUBLE PRECISION, 
            AtomStateDescription VARCHAR(128))'''
        c.execute(ATOMSTATE_CREATE)
        conn.commit()
        
        if Atoms: 
            c = conn.cursor()   
            ATOMS_INSERT = ''' INSERT INTO Atoms(
                'AtomSpeciesId',
                'AtomSymbol',
                'AtomNuclearCharge',
                'AtomIonCharge',
                'AtomInchi',
                'AtomInchiKey')
                VALUES(?,?,?,?,?,?) '''
            ATOMSTATE_INSERT = '''INSERT INTO AtomicStates(
                'AtomStateId',
                'AtomRef',
                'AtomStateTotalAngMom',
                'AtomStateParity',
                'AtomStateStatisticalWeight',
                'AtomStateEnergy',
                'AtomStateDescription')
                VALUES(?,?,?,?,?,?,?)'''
            for a in Atoms.all().iterator():
                c.execute(ATOMS_INSERT, (a.id, a.atomsymbol, a.atomnuclearcharge, a.atomioncharge, a.inchi, a.inchikey))
                if not hasattr(a,'States'):
                    a.States = []
                for s in a.States:
                    c.execute(ATOMSTATE_INSERT,
                        (s.id, a.id, s.atomstatetotalangmom, s.parity, s.statisticalweight, s.energy, s.atomstateconfigurationlabel)
                    )
                conn.commit()
    finally:
        if conn:
            conn.close()


def cleandict(indict):
    """
    throw out some keys
    """
    return {k:v for k,v in indict.items() if (v and not '.' in k)}


def capabilities(request):
    c = {"accessURL" : getBaseURL(request),
                                 "RESTRICTABLES" : cleandict(DICTS.RESTRICTABLES),
                                 "RETURNABLES" : cleandict(DICTS.RETURNABLES),
                                 "STANDARDS_VERSION" : settings.VAMDC_STDS_VERSION,
                                 "SOFTWARE_VERSION" : settings.NODESOFTWARE_VERSION,
                                 "EXAMPLE_QUERIES" : settings.EXAMPLE_QUERIES,
                                 "MIRRORS" : settings.MIRRORS,
                                 "APPS" : settings.VAMDC_APPS,
                                 }
    return render(request, template_name='tap/capabilities.xml', context=c, content_type='text/xml')


from django.db import connection
def dbConnected():
    try:
        cursor=connection.cursor()
        return ('true', 'service is available, database is connected.')
    except Exception as oops:
        log.error(oops)
        return ('false', 'database is not connected')

def availability(request):
    (status, message) = dbConnected()
    c={"accessURL" : getBaseURL(request), 'ok' : status, 'message' : message}
    return render(request, template_name='tap/availability.xml', context=c, content_type='text/xml')

def tables(request):
    c={"column_names_list" : DICTS.RETURNABLES.keys(), 'baseURL' : getBaseURL(request)}
    return render(request, template_name='tap/VOSI-tables.xml', context=c, content_type='text/xml')
    
def job(request, id=None):
    if id:
        if request.method == 'GET':
            j = Job.objects.filter(id=id)[0]
            try:
                filePath = settings.RESULTS_CACHE_DIR + os.path.sep + j.file
                sizeInBytes = int(os.path.getsize(filePath))
            except:
                sizeInBytes = 0
            c = {'job': j, 'file_bytes': sizeInBytes}
            return render(request, template_name='tap/job.html', context=c, content_type='text/html')
        elif (request.method == 'POST') or (request.method == 'DELETE'):
            Job.objects.filter(id=id).delete()
            return redirect('/tap/async/jobs')
        else:
            return HttpResponse(status=400)
    else:
        return HttpResponse(status=404);
        
def result(request, id=None):
    if id:
        filePath = settings.RESULTS_CACHE_DIR + os.path.sep + str(id) + '.sqlite3'
        return FileResponse(open(filePath, 'rb'))
    else:
        return HttpResponse(status=404);
        
def jobs(request):
    c = {'jobs': Job.objects.all()}
    return render(request, template_name='tap/jobs.html', context=c, content_type='text/html')
    
def form(request):
    return render(request, template_name='tap/async-query.html', content_type='text/html')

