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

PARA_CHOICES=[(1,u''),
              (2,u'Atomic number'),
              (3,u'Ionization'),
              (4,u'Wavelength in vaccum (Å)'),
              (5,u'Wavelength in air (Å)'),
              (6,u'log(g*f)'),
              (7,u'Level energy (1/cm)'),
              (8,u'Species from species list (not implemented)'),
              (9,u'Total angular momentum J'),
]

class ConditionForm(forms.Form):
    lower=forms.DecimalField(max_digits=8,required=False,initial=None,label='lower bound')
    parameter=forms.ChoiceField(label='parameter to restrict',required=True,initial='',choices=PARA_CHOICES)
    upper=forms.DecimalField(max_digits=8,required=False,initial=None,label='upper bound')
    connection=forms.BooleanField(initial=True,required=False,label='Use AND to connect with next condition?')
    
    def validate(self,value):
        super(ConditionForm,self).validate(value)

              


class OutputForm(forms.Form):
    pass

class SQLqueryForm(forms.Form):
    sql=forms.CharField()

def query(request):
    ConditionSet = formset_factory(ConditionForm, extra=5)
    if request.method == 'POST':
        print request.POST
        selectionset = ConditionSet(request.POST,request.FILES) 
        if selectionset.is_valid(): 
            return HttpResponseRedirect('http://vamdc.fysast.uu.se:8888/node/vald/tap/sync/?REQUEST=doQuery&LANG=ADQL&FORMAT=XSAMS&QUERY=SELECT%20ALL%20WHERE%20WAVELENGTH%20%3E%203000%20AND%20WAVELENGTH%20%3C%203500%20AND%20ELEMENT%20=%20Fe',) 
    else:
        selectionset = ConditionSet(initial=[
                {'lower': u'3000',
                 'upper': u'3500',
                 'parameter':4,
                 'connection':True,
                 },
                {'lower': u'26',
                 'upper': u'26',
                 'parameter':2,
                 'connection':True,
                 },
                ])
        
    return render_to_response('portal/query.html', {
                                                    'selectionset': selectionset,
                                                    })
