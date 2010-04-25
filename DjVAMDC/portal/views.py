# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response,get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django import forms
from django.forms.formsets import formset_factory

import urllib

def index(request):
    c=RequestContext(request,{})
    return render_to_response('portal/index.html', c)

PARA_CHOICES=[u'Atomic number',u'Ionization',u'Wavelength in vaccum (Å)',u'Wavelength in air (Å)',u'log(g*f)',u'Level energy (1/cm)',u'Species from species list (not implemented)',u'Total angular momentum J']

class ConditionForm(forms.Form):
    pass

class OutputForm(froms.Form):
    pass

class SQLqueryForm(forms.Form):
    sql=forms.CharField()

def query(request):
    if request.method == 'POST': # If the form has been submitted...
        form = QueryForm(request.POST) # A form bound to the POST data
        if form.is_valid(): 
            return HttpResponseRedirect('http://vamdc.fysast.uu.se:8888/node/vald/tap/sync/?REQUEST=doQuery&LANG=ADQL&FORMAT=XSAMS&QUERY=SELECT%20ALL%20WHERE%20WAVELENGTH%20%3E%203000%20AND%20WAVELENGTH%20%3C%203500%20AND%20ELEMENT%20=%20Fe',) 
    else:
        form = QueryForm() # An unbound form

    return render_to_response('portal/query.html', {
                                                    'form': form,
                                                    })
