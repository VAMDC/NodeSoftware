# -*- coding: utf-8 -*-

# This is where you would add additional functionality to your node, 
# bound to certain URLs in urls.py

from django.template import RequestContext
from django.shortcuts import render_to_response,get_object_or_404

from cdmsportalfunc import *

def index(request):
    c=RequestContext(request,{})
#    return render_to_response('tap/index.html', c)
    return render_to_response('cdms/portalBase.html', c)


def index2(request):
    c=RequestContext(request,{})
    return render_to_response('tap/index.html', c)
        
        
def queryPage(request):
    test = request.POST
    id_list = request.POST.getlist('speciesIDs')
    
    species_list = getSpeciesList(id_list)
    c=RequestContext(request,{"postvar" : test, "speciesid_list": id_list, "species_list" : species_list})
    return render_to_response('cdms/queryForm.html', c)


def queryForm(request):
    """
    Create the species selection - page from the species (model) stored in the database
    """
    species_list = getSpeciesList()
    c=RequestContext(request,{"test" : " sfasdfasdf test", "species_list" : species_list})
    return render_to_response('cdms/querySpecies.html', c)


def showResults(request):
    """
    """
    c=RequestContext(request,{"query" : ""})
    return render_to_response('cdms/showResults.html', c)
