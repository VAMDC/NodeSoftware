# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.forms import Form,FileField,URLField

class ConversionForm(Form):
    infile = FileField(label='Input file')
    inurl = URLField(label='Input URL')


def handle_file():
    pass

def handle_url():
    pass

def xsams2sme(request):
    if request.method == 'POST':
        ConvForm = ConversionForm(request.POST, request.FILES)
        if ConvForm.is_valid():
            print ConvForm.cleaned_data
           #ConvForm.save()
           #return HttpResponseRedirect('/')
    else:
        ConvForm = ConversionForm()
    c=RequestContext(request,{'conversion':ConvForm})
    return render_to_response('webtools/xsams2sme.html', c)

