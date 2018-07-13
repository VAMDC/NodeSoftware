# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import loader
from django.http import HttpResponse, StreamingHttpResponse

import datetime
import uuid
import os, math, sys
from base64 import b64encode
randStr = lambda n: b64encode(os.urandom(int(math.ceil(0.75*n))))[:n]
import time

import logging
log = logging.getLogger('vamdc.tap')

from django.conf import settings
from importlib import import_module
from django.utils.http import http_date
from requests.utils import CaseInsensitiveDict as CaselessDict
from django.db import connection

if settings.QUERY_STORE_ACTIVE:
    try:
        import requests as librequests
    except:
        log.critical('settings.QUERY_STORE_ACTIVE is True but requests package is missing!')

QUERYFUNC = import_module(settings.NODEPKG + '.queryfunc')
DICTS = import_module(settings.NODEPKG + '.dictionaries')

# import helper modules that reside in the same directory
NODEID = CaselessDict(DICTS.RETURNABLES)['NodeID']
from .generators import *
from .sqlparse import SQL

REQUESTABLES = [req.lower() for req in [
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
 'States']]


# This turns a 404 "not found" error into a TAP error-document
def tapNotFoundError(request):
    text = 'Resource not found: %s' % request.path
    document = loader.get_template('tap/TAP-error-document.xml').render({"error_message_text": text})
    return HttpResponse(document, status=404, content_type='text/xml')


# This turns a 500 "internal server error" into a TAP error-document
def tapServerError(request=None, status=500, errmsg=''):
    text = 'Error in TAP service: %s' % errmsg
    document = loader.get_template('tap/TAP-error-document.xml').render({"error_message_text": text})
    return HttpResponse(document, status=status, content_type='text/xml')


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

    def __init__(self, request):
        if 'X_REQUEST_METHOD' in request.META:  # workaround for mod_wsgi
            self.XRequestMethod = request.META['X_REQUEST_METHOD']
        self.HTTPmethod = request.method
        self.isvalid = True
        self.errormsg = ''
        self.token = request.token
        try:
            self.request = CaselessDict(dict(request.GET or request.POST))
        except Exception as e:
            self.isvalid = False
            self.errormsg = 'Could not read argument dict: %s' % e
            log.error(self.errormsg)

        if self.isvalid:
            self.validate()

        self.fullurl = getBaseURL(request) + 'sync?' + request.META.get('QUERY_STRING')

    def validate(self):
        try:
            self.lang = self.request['LANG'][0]
            self.lang = self.lang.lower()
        except:
            log.debug('LANG is empty, assuming VSS2')
            self.lang = 'vss2'
        else:
            if self.lang not in ('vss1', 'vss2'):
                self.errormsg += 'Only LANG=VSS1 or LANG=VSS2 is supported.\n'

        try: self.query = self.request['QUERY'][0]
        except: self.errormsg += 'Cannot find QUERY in request.\n'

        try:
            self.format = self.request['FORMAT'][0]
            self.format = self.format.lower()
        except:
            log.debug('FORMAT is empty, assuming XSAMS')
            self.format = 'xsams'
        else:
            if self.format != 'xsams':
                log.debug('Requested FORMAT is not XSAMS, letting it pass anyway.')
        try: self.parsedSQL = SQL.parseString(self.query, parseAll=True)
        except: # if this fails, we're done
            self.errormsg += 'Could not parse the SQL query string: %s\n'%getattr(self,'query',None)
            self.isvalid = False
            return

        self.requestables = set()
        self.where = self.parsedSQL.where
        if self.parsedSQL.columns not in ('*', 'ALL'):
            for r in self.parsedSQL.columns:
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
            self.isvalid = False

    def __str__(self):
        return '%s' % self.query


def addHeaders(headers, request, response):
    HEADS = ['COUNT-SOURCES',
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
                log.warn('Query Store unreachable! %s' % e)
            else:
                if logreq.status_code != 200:
                  log.warn('Query Store returned code: %s' % logreq.status_code)
                  log.debug('QS reply text:\n%s' % logreq.text)
        return response
    return wrapper


@logCentral
def sync(request):

    request.token = "%s:%s:%s" % (settings.NODENAME, uuid.uuid4(), request.method.lower())

    if request.method == 'OPTIONS':
        return CORS_request(request)

    log.info('Request from %s: %s' % (request.META['REMOTE_ADDR'], request.GET or request.POST))
    tap = TAPQUERY(request)
    if not tap.isvalid:
        emsg = 'TAP-Request invalid: %s' % tap.errormsg
        log.error(emsg)
        return tapServerError(status=400, errmsg=emsg)

    # if the requested format is not XSAMS, hand over to the node QUERYFUNC
    if tap.format != 'xsams' and hasattr(QUERYFUNC, 'returnResults'):
        log.debug("using custom QUERYFUNC.returnResults(tap)")
        return QUERYFUNC.returnResults(tap)

    # otherwise, setup the results and build the XSAMS response here
    try:
        querysets = QUERYFUNC.setupResults(tap)
    except Exception as err:
        emsg = 'Query processing in setupResults() failed: %s' % err
        log.debug(emsg)
        return tapServerError(status=400, errmsg=emsg)

    if not querysets:
        log.info('setupResults() gave something empty. Returning 204.')
        response=HttpResponse('', status=204)
        response['Access-Control-Allow-Origin'] = '*'
        return response

    if request.method in ['GET', 'POST']:
        if hasattr(QUERYFUNC, 'customXsams'):
            log.debug("using QUERYFUNC.customXsams as generator")
            generator = QUERYFUNC.customXsams(tap=tap, **querysets)
        else:
            generator = Xsams(tap=tap, **querysets)
        response = StreamingHttpResponse(generator, content_type='text/xml')
        response['Content-Disposition'] = 'attachment; filename=%s-%s.%s' % (NODEID,
            datetime.datetime.now().isoformat(), tap.format)
    elif request.method == 'HEAD':
        response = HttpResponse('', status=204)
    else:
        emsg = 'Unauthorized method %s' % request.method
        return tapServerError(status=405, errmsg=emsg)



    headers = querysets.get('HeaderInfo') or {}
    headers["REQUEST-TOKEN"] = request.token

    response = addHeaders(headers, request, response)

    # Override with empty response if result is empty
    if 'VAMDC-APPROX-SIZE' in response:
        try:
            size = float(response['VAMDC-APPROX-SIZE'])
            if size == 0.0:
                log.info('Empty result')
                response.status_code = 204
                return response
        except Exception as e:
            pass

    return response


def cleandict(indict):
    """
    throw out some keys
    """
    return {k: v for k, v in indict.items() if (v and not '.' in k)}


def capabilities(request):
    c = {"accessURL": getBaseURL(request),
                                 "RESTRICTABLES": cleandict(DICTS.RESTRICTABLES),
                                 "RETURNABLES": cleandict(DICTS.RETURNABLES),
                                 "STANDARDS_VERSION": settings.VAMDC_STDS_VERSION,
                                 "SOFTWARE_VERSION": settings.NODESOFTWARE_VERSION,
                                 "EXAMPLE_QUERIES": settings.EXAMPLE_QUERIES,
                                 "MIRRORS": settings.MIRRORS,
                                 "APPS": settings.VAMDC_APPS,
                                 }
    return render_to_response('tap/capabilities.xml', c, content_type='text/xml')


def dbConnected():
    try:
        cursor = connection.cursor()
        return ('true', 'service is available, database is connected.')
    except:
        return ('false', 'database is not connected')


def availability(request):
    (status, message) = dbConnected()
    c={"accessURL" : getBaseURL(request), 'ok' : status, 'message' : message}
    return render_to_response('tap/availability.xml', c, content_type='text/xml')


def tables(request):
    c={"column_names_list": DICTS.RETURNABLES.keys(), 'baseURL': getBaseURL(request)}
    return render_to_response('tap/VOSI-tables.xml', c, content_type='text/xml')

