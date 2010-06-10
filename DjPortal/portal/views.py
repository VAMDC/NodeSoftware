# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response,get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django import forms
from django.forms.formsets import formset_factory

from DjPortal.portal.models import Query

import string as s
from random import choice
def makeQID(length=6, chars=s.letters + s.digits):
    return ''.join([choice(chars) for i in xrange(length)])

from urllib import urlopen,urlencode

REGISTRY=[
          {'name':'VALD','url':'http://vamdc.fysast.uu.se:8888/node/vald/tap/sync/'},
          {'name':'CDMS','url':'http://www.astro.uni-koeln.de:8098/DjCDMS/tap/sync/'},
          ]

PARA_CHOICES=[('',u''),
#              ('',u'Atomic number'),
#              ('',u'Ionization'),
              ('RadTransWavelengthExperimentalValue',u'(Radiative transition) Wavelength in vaccum (Å)'),
              ('RadTransProbabilityLog10WeightedOscillatorStrengthValue',u'(Radiative transition) Oscillator strength, log(g*f)'),
#              ('',u'Level energy (1/cm)'),
#              ('',u'Species from species list (not implemented)'),
]

class ConditionForm(forms.Form):
    lower=forms.DecimalField(max_digits=6,required=False,initial=None,label='lower bound',widget=forms.widgets.TextInput(attrs={'size':'8'}))
    parameter=forms.ChoiceField(label='parameter to restrict',required=True,initial='',choices=PARA_CHOICES)
    upper=forms.DecimalField(max_digits=6,required=False,initial=None,label='upper bound',widget=forms.widgets.TextInput(attrs={'size':'8'}))
    connection=forms.BooleanField(initial=True,required=False,label='Use AND to connect with next condition?')
    
    def validate(self,value):
        # check here e.g. if the lower bound <= upper
        super(ConditionForm,self).validate(value)              

def constructQuery(constraints):
    q='select all where '
    for c in constraints:
        print c
        if c == {}: continue
        if not c['parameter']: continue
        if c['lower'] and c['upper']:
            if c['lower'] == c['upper']: q+='( %%(%s)s = %s )'%(c['parameter'],c['upper'])
            else:
                q+='( %%(%s)s > %s and '%(c['parameter'],c['lower'])
                q+='%%(%s)s < %s )'%(c['parameter'],c['upper'])
        elif c['lower']:
            q+='( %%(%s)s > %s )'%(c['parameter'],c['lower'])
        elif c['upper']:
            q+='( %%(%s)s < %s )'%(c['parameter'],c['upper'])
        else:
            q+='( %%(%s)s notnull )'%c['parameter']

        if c['connection']: q+=' AND '
        else: q+=' OR  '
    return q[:-5] # remove the last AND/OR

def query(request):
    ConditionSet = formset_factory(ConditionForm, extra=5)
    if request.method == 'POST':
        selectionset = ConditionSet(request.POST,request.FILES) 
        if selectionset.is_valid():
            query=Query(qid=makeQID(),query=constructQuery(selectionset.cleaned_data))
            query.save()
            return HttpResponseRedirect('/portal/results/%s/'%query.qid) 
    else:
        selectionset = ConditionSet(initial=[
                {'lower': u'5000',
                 'upper': u'5050',
                 'parameter':'RadTransWavelengthExperimentalValue',
                 'connection':True,
                 },
                ])
        
    return render_to_response('portal/query.html', {'selectionset': selectionset})


#####################

def askNodeForCount(url,query):
    data={}
    data['LANG']='VAMDC'
    data['REQUEST']='doQuery'
    data['QUERY']=query
    data['FORMAT']='count'
    data=urlencode(data)
    req=urlopen(url,data)
    html=req.read()
    req.close()
    return html

def makeDlLink(url,query,format='XSAMS'):
    data={}
    data['LANG']='VAMDC'
    data['REQUEST']='doQuery'
    data['QUERY']=query
    data['FORMAT']=format
    data=urlencode(data)
    return url+'?'+data
    
def results(request,qid):
    query=Query.objects.get(pk=qid)
    results=[]
    for node in REGISTRY:
        result={'nodename':node['name']}
        result['count']=askNodeForCount(node['url'],query.query)
        #result['html']=askNodeForEmbedHTML(node['url'],query.query)
        #result['vourl']=makeDlLink(node['url'],query.query,format='VOTABLE')
        result['xsamsurl']=makeDlLink(node['url'],query.query,format='XSAMS')
        results.append(result)
        
    return render_to_response('portal/results.html', {'results': results, 
                                                      'query':query,
                                                      })

###################

def index(request):
    c=RequestContext(request,{})
    return render_to_response('portal/index.html', c)

######################

class SQLqueryForm(forms.Form):
    sql=forms.CharField(label='Enter your SQL query',widget=forms.widgets.Textarea(attrs={'cols':'40','rows':'5'}),required=True)


def sqlquery(request):
    if request.method == 'POST':
        form = SQLqueryForm(request.POST) 
        if form.is_valid():
            print form.cleaned_data

    else:
        form=SQLqueryForm()
        
    return render_to_response('portal/sqlquery.html', {'form': form})

