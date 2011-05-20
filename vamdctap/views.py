# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response,get_object_or_404
from django.template import RequestContext, Context, loader
from django.http import HttpResponseRedirect, HttpResponse
from django.db.models import Q

from datetime import date
from string import lower
from cStringIO import StringIO
import os, math, sys
from base64 import b64encode
randStr = lambda n: b64encode(os.urandom(int(math.ceil(0.75*n))))[:n]

import logging
LOG=logging.getLogger('vamdc.tap')

# Get the node-specific package!
from django.conf import settings
from django.utils.importlib import import_module
QUERYFUNC=import_module(settings.NODEPKG+'.queryfunc')
DICTS=import_module(settings.NODEPKG+'.dictionaries')

# import helper modules that reside in the same directory
from generators import *
from sqlparse import SQL
from caselessdict import CaselessDict

class TAPQUERY(object):
    """
    This class holds the query, does some validation
    and triggers the SQL parser.
    """
    def __init__(self,data):
        try:
            data=CaselessDict(dict(data))
            self.lang=lower(data['LANG'])
            self.query=data['QUERY']
            self.format=lower(data['FORMAT'])
            self.isvalid=True
        except Exception,e:
            self.isvalid=False
            LOG.error(str(e))

        if self.isvalid: self.validate()
        if self.isvalid: self.assignQID()
	#if self.isvalid: self.makeQtup()
        if self.isvalid: self.parseSQL()

    def validate(self):
        """
        overwrite this method for
        custom checks, depending on data set
        """

    def parseSQL(self):
        self.parsedSQL=SQL.parseString(self.query)

    def assignQID(self):
        """ make a query-id """
        self.queryid='%s-%s'%(date.today().isoformat(),randStr(8))

    def __str__(self):
        return '%s'%self.query

def getBaseURL(request):
    return 'http://' + request.get_host() + request.path.split('/tap',1)[0] + '/tap/'

def addHeaders(headers,response):
    HEADS=['COUNT-SOURCES',
           'COUNT-SPECIES',
           'COUNT-STATES',
           'COUNT-COLLISIONS',
           'COUNT-RADIATIVE',
           'COUNT-NONRADIATIVE',
           'TRUNCATED']

    for h in HEADS:
        if headers.has_key(h):
            if headers[h]: response['VAMDC-'+h] = '%s'%headers[h]
    return response

def sync(request):
    tap=TAPQUERY(request.REQUEST)
    if not tap.isvalid:
        # return http error
        LOG.warning('not valid tap!')

#    if tap.format == 'xsams':  # for now always assume we want XSAMS    
    results=QUERYFUNC.setupResults(tap.parsedSQL)
    generator=Xsams(**results)
    response=HttpResponse(generator,mimetype='text/xml')
    #response['Content-Disposition'] = 'attachment; filename=%s.%s'%(tap.queryid,tap.format)

    if results.has_key('HeaderInfo'):
        response=addHeaders(results['HeaderInfo'],response)


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
                                 })
    return render_to_response('node/capabilities.xml', c, mimetype='text/xml')

def tables(request):
    c=RequestContext(request,{"column_names_list" : DICTS.RETURNABLES.keys(), 'baseURL' : getBaseURL(request)})
    return render_to_response('node/VOSI-tables.xml', c, mimetype='text/xml')

def availability(request):
    c=RequestContext(request,{})
    return render_to_response('node/availability.xml', c, mimetype='text/xml')

def availabilityXsl(request):
    c = RequestContext(request, {})
    return render_to_response('node/Availability.xsl', c, mimetype='text/xsl')

def tablesXsd(request):
    c = RequestContext(request,{})
    return render_to_response('static/xsd/Tables.xsd', c)

def capabilitiesXsd(request):
    c = RequestContext(request, {})
    return render_to_response('node/Capabilities.xsd', c)

def capabilitiesXsl(request):
    c = RequestContext(request, {})
    return render_to_response('node/Capabilities.xsl', c)

def index(request):
    c=RequestContext(request,{})
    return render_to_response('node/index.html', c)

# This turns a 404 "not found" error into a TAP error-document
def tapNotFoundError(request):
    text = 'Resource not found: %s'%request.path();
    document = loader.get_template('node/TAP-error-document.xml').render(Context({"error_message_text" : text}))
    return HttpResponse(document, status=404, mimetype='text/xml');

# This turns a 500 "internal server error" into a TAP error-document
def tapServerError(request):
    text = 'Unknown error inside TAP service';
    document = loader.get_template('node/TAP-error-document.xml').render(Context({"error_message_text" : text}))
    return HttpResponse(document, status=500, mimetype='text/xml');
