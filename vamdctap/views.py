# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response,get_object_or_404
from django.template import RequestContext, Context, loader
from django.http import HttpResponseRedirect, HttpResponse

from datetime import datetime
from string import lower
from cStringIO import StringIO
import os, math, sys
from base64 import b64encode
randStr = lambda n: b64encode(os.urandom(int(math.ceil(0.75*n))))[:n]
import time

import logging
log=logging.getLogger('vamdc.tap')

# Get the node-specific package!
from django.conf import settings
from django.utils.importlib import import_module
from django.utils.http import http_date

QUERYFUNC = import_module(settings.NODEPKG+'.queryfunc')
DICTS = import_module(settings.NODEPKG+'.dictionaries')

# import helper modules that reside in the same directory
from caselessdict import CaselessDict
NODEID = CaselessDict(DICTS.RETURNABLES)['NodeID']
from generators import *
from sqlparse import SQL

REQUESTABLES = map(lower, [\
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
 'States'] )


# This turns a 404 "not found" error into a TAP error-document
def tapNotFoundError(request):
    text = 'Resource not found: %s'%request.path;
    document = loader.get_template('tap/TAP-error-document.xml').render(Context({"error_message_text" : text}))
    return HttpResponse(document, status=404, mimetype='text/xml');

# This turns a 500 "internal server error" into a TAP error-document
def tapServerError(request=None, status=500, errmsg=''):
    text = 'Error in TAP service: %s'%errmsg
    document = loader.get_template('tap/TAP-error-document.xml').render(Context({"error_message_text" : text}))
    return HttpResponse(document, status=status, mimetype='text/xml');

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
        self.isvalid = True
        self.errormsg = ''
        try:
            self.request=CaselessDict(dict(request.REQUEST))
        except Exception,e:
            self.isvalid = False
            self.errormsg = 'Could not read argument dict: %s'%e
            log.error(self.errormsg)

        if self.isvalid: self.validate()
        self.fullurl = getBaseURL(request) + 'sync?' + request.META.get('QUERY_STRING')

    def validate(self):
        try: self.lang = lower(self.request['LANG'])
        except: self.errormsg = 'Cannot find LANG in request.\n'
        else:
            if self.lang not in ('vss1','vss2'):
                self.errormsg += 'Only LANG=VSS1 or LANG=VSS2 is supported.\n'

        try: self.query = self.request['QUERY']
        except: self.errormsg += 'Cannot find QUERY in request.\n'

        try: self.format=lower(self.request['FORMAT'])
        except: self.errormsg += 'Cannot find FORMAT in request.\n'

        try: self.parsedSQL=SQL.parseString(self.query,parseAll=True)
        except: # if this fails, we're done
            self.errormsg += 'Could not parse the SQL query string: %s\n'%self.query
            self.isvalid=False
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

        if self.errormsg: self.isvalid=False

    def __str__(self):
        return '%s'%self.query

def addHeaders(headers,response):
    HEADS=['COUNT-SOURCES',
           'COUNT-ATOMS',
           'COUNT-MOLECULES',
           'COUNT-SPECIES',
           'COUNT-STATES',
           'COUNT-COLLISIONS',
           'COUNT-RADIATIVE',
           'COUNT-NONRADIATIVE',
           'TRUNCATED',
           'APPROX-SIZE']

    headers = CaselessDict(headers)

    try:
        response['Last-Modified'] = getFormatLastModified(headers['LAST-MODIFIED'])
    except:
        pass

    for h in HEADS:
        if headers.has_key(h):
            response['VAMDC-'+h] = '%s'%headers[h]

    if headers.has_key('LAST-MODIFIED'):
        response['Last-Modified'] = '%s'%headers['LAST-MODIFIED']

    return response

def sync(request):
    log.info('Request from %s: %s'%(request.META['REMOTE_ADDR'],request.REQUEST))
    tap=TAPQUERY(request)
    if not tap.isvalid:
        emsg = 'TAP-Request invalid: %s'%tap.errormsg
        log.error(emsg)
        return tapServerError(status=400,errmsg=emsg)

    # if the requested format is not XSAMS, hand over to the node QUERYFUNC
    if tap.format != 'xsams' and hasattr(QUERYFUNC,'returnResults'):
        return QUERYFUNC.returnResults(tap)

    # otherwise, setup the results and build the XSAMS response here
    try: querysets = QUERYFUNC.setupResults(tap)
    except Exception, err:
        emsg = 'Query processing in setupResults() failed: %s'%err
        log.debug(emsg)
        return tapServerError(status=400,errmsg=emsg)

    if not querysets:
        log.info('setupResults() gave something empty. Returning 204.')
        return HttpResponse('', status=204)

    log.debug('Requestables: %s'%tap.requestables)
    generator=Xsams(tap=tap,**querysets)
    log.debug('Generator set up, handing it to HttpResponse.')
    response=HttpResponse(generator,mimetype='text/xml')
    response['Content-Disposition'] = 'attachment; filename=%s-%s.%s'%(NODEID, datetime.now().isoformat(), tap.format)

    if 'HeaderInfo' in querysets:
        response=addHeaders(querysets['HeaderInfo'],response)

        # Override with empty response if result is empty
        if 'VAMDC-APPROX-SIZE' in response:
            try:
                size = float(response['VAMDC-APPROX-SIZE'])
                if size == 0.0:
                    log.info('Empty result')
                    return HttpResponse('', status=204)
            except: pass
    else:
        log.warn('Query function did not return information for HTTP-headers.')

#    elif tap.format == 'votable':
#        transs,states,sources=QUERYFUNC.setupResults(tap)
#        generator=votable(transs,states,sources)
#        response=HttpResponse(generator,mimetype='text/xml')

    return response

def cleandict(dict):
    """
    throw out keys where the value is ''
    """
    ret={}
    for key in dict.keys():
        if dict[key]: ret[key]=dict[key]
    return ret


def capabilities(request):
    c = RequestContext(request, {"accessURL" : getBaseURL(request),
                                 "RESTRICTABLES" : cleandict(DICTS.RESTRICTABLES),
                                 "RETURNABLES" : cleandict(DICTS.RETURNABLES),
                                 "STANDARDS_VERSION" : settings.VAMDC_STDS_VERSION,
                                 "SOFTWARE_VERSION" : settings.NODESOFTWARE_VERSION,
                                 "EXAMPLE_QUERIES" : settings.EXAMPLE_QUERIES,
                                 "MIRRORS" : settings.MIRRORS,
                                 })
    return render_to_response('tap/capabilities.xml', c, mimetype='text/xml')

def availability(request):
    c=RequestContext(request,{"accessURL" : getBaseURL(request)})
    return render_to_response('tap/availability.xml', c, mimetype='text/xml')

def tables(request):
    c=RequestContext(request,{"column_names_list" : DICTS.RETURNABLES.keys(), 'baseURL' : getBaseURL(request)})
    return render_to_response('tap/VOSI-tables.xml', c, mimetype='text/xml')

#def index(request):
#    c=RequestContext(request,{})
#    return render_to_response('tap/index.html', c)
#
#def async(request):
#    c=RequestContext(request,{})
#    return render_to_response('tap/index.html', c)

