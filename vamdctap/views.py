# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response,get_object_or_404
from django.template import RequestContext, Context, loader
from django.http import HttpResponseRedirect, HttpResponse
from django.db.models import Q

from datetime import datetime
from string import lower
from cStringIO import StringIO
import os, math, sys
from base64 import b64encode
randStr = lambda n: b64encode(os.urandom(int(math.ceil(0.75*n))))[:n]

import logging
log=logging.getLogger('vamdc.tap')
log.debug('test log start')

# Get the node-specific package!
from django.conf import settings
from django.utils.importlib import import_module
QUERYFUNC = import_module(settings.NODEPKG+'.queryfunc')
DICTS = import_module(settings.NODEPKG+'.dictionaries')

# import helper modules that reside in the same directory
from caselessdict import CaselessDict
NODEID = CaselessDict(DICTS.RETURNABLES)['NodeID']
from generators import *
from sqlparse import SQL

# This turns a 404 "not found" error into a TAP error-document
def tapNotFoundError(request):
    text = 'Resource not found: %s'%request.path;
    document = loader.get_template('node/TAP-error-document.xml').render(Context({"error_message_text" : text}))
    return HttpResponse(document, status=404, mimetype='text/xml');

# This turns a 500 "internal server error" into a TAP error-document
def tapServerError(request=None, status=500, errmsg=''):
    text = 'Error in TAP service: %s'%errmsg
    document = loader.get_template('node/TAP-error-document.xml').render(Context({"error_message_text" : text}))
    return HttpResponse(document, status=status, mimetype='text/xml');


class TAPQUERY(object):
    """
    This class holds the query, does some validation
    and triggers the SQL parser.
    """
    def __init__(self,data):
        self.isvalid = True
        self.errormsg = ''
        try:
            self.data=CaselessDict(dict(data))
        except Exception,e:
            self.isvalid = False
            self.errormsg = 'Could not read argument dict: %s'%e
            log.error(self.errormsg)

        if self.isvalid: self.validate()

    def validate(self):
        try: self.lang = lower(self.data['LANG'])
        except: self.errormsg = 'Cannot find LANG in request.\n'
        else:
            if self.lang != 'vss1':
                self.errormsg += 'Currently, only LANG=VSS1 is supported.\n'

        try: self.query = self.data['QUERY']
        except: self.errormsg += 'Cannot find QUERY in request.\n'

        try: self.format=lower(self.data['FORMAT'])
        except: self.errormsg += 'Cannot find FORMAT in request.\n'
        #else:
            #if self.format != 'xsams':
            #    self.errormsg += 'Currently, only FORMAT=XSAMS is supported.\n'

        try: self.parsedSQL=SQL.parseString(self.query)
        except: self.errormsg += 'Could not parse the SQL query string.\n'

        if self.errormsg: self.isvalid=False

    def __str__(self):
        return '%s'%self.query

def getBaseURL(request):
    return 'http://' + request.get_host() + request.path.split('/tap',1)[0] + '/tap/'

def addHeaders(headers,response):
    HEADS=['COUNT-SOURCES',
           'COUNT-ATOMS',
           'COUNT-MOLECULES',
           'COUNT-STATES',
           'COUNT-COLLISIONS',
           'COUNT-RADIATIVE',
           'COUNT-NONRADIATIVE',
           'TRUNCATED',
           'APPROX-SIZE']

    headers = CaselessDict(headers)

    for h in HEADS:
        if headers.has_key(h):
            if headers[h]: response['VAMDC-'+h] = '%s'%headers[h]
    return response

def sync(request):
    log.info('Request from %s: %s'%(request.META['REMOTE_ADDR'],request.REQUEST))
    tap=TAPQUERY(request.REQUEST)
    if not tap.isvalid:
        emsg = 'TAP-Request invalid: %s'%tap.errormsg
        log.error(emsg)
        return tapServerError(status=400,errmsg=emsg)

    # if the requested format is not XSAMS, hand over to the node QUERYFUNC
    if tap.format != 'xsams':
        return QUERYFUNC.returnResults(tap)
    # otherwise, setup the results and build the XSAMS response here
    results=QUERYFUNC.setupResults(tap.parsedSQL)
    if not results:
        log.info('setupResults() gave something empty. Returning 204.')
        return HttpResponse('', status=204)

    generator=Xsams(**results)
    response=HttpResponse(generator,mimetype='text/xml')
    response['Content-Disposition'] = 'attachment; filename=%s-%s.%s'%(NODEID, datetime.now().isoformat(), tap.format)

    if 'HeaderInfo' in results:
        response=addHeaders(results['HeaderInfo'],response)

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

def async(request):
    c=RequestContext(request,{})
    return render_to_response('node/index.html', c)

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
                                 })
    return render_to_response('tap/capabilities.xml', c, mimetype='text/xml')

def availability(request):
    c=RequestContext(request,{"accessURL" : getBaseURL(request)})
    return render_to_response('tap/availability.xml', c, mimetype='text/xml')

def tables(request):
    c=RequestContext(request,{"column_names_list" : DICTS.RETURNABLES.keys(), 'baseURL' : getBaseURL(request)})
    return render_to_response('tap/VOSI-tables.xml', c, mimetype='text/xml')

def index(request):
    c=RequestContext(request,{})
    return render_to_response('node/index.html', c)

