# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.forms import Form,FileField,URLField,TextInput
from django.core.exceptions import ValidationError

from lxml import etree as e
xsl=e.XSLT(e.parse(open('xsams2sme/xsams2sme.xsl')))

from urllib2 import urlopen

class ConversionForm(Form):
    infile = FileField(label='Input file',required=False)
    inurl = URLField(label='Input URL',required=False,widget=TextInput(attrs={'size': 100, 'title': 'Paste here a URL that delivers an XSAMS document.',}))

    def clean(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('infile') and cleaned_data.get('inurl')\
            or (not (cleaned_data.get('infile') or cleaned_data.get('inurl'))):
            raise ValidationError('Give either input file or URL!')

        return cleaned_data

def handle_file(data):
    return xsl(e.parse(data))

def handle_url(url):
    data = urlopen(url)
    return xsl(e.parse(data))

def xsams2sme(request):
    if request.method != 'POST':
        ConvForm = ConversionForm()
    else:
        ConvForm = ConversionForm(request.POST, request.FILES)
        if ConvForm.is_valid():
            infile=ConvForm.cleaned_data.get('infile')
            inurl=ConvForm.cleaned_data.get('inurl')
            if infile:
                data = handle_file(infile)
            elif inurl:
                data = handle_url(inurl)
            response=HttpResponse(data,mimetype='text/csv')
            response['Content-Disposition'] = \
                'attachment; filename=%s.sme'% (getattr(infile, 'name', None) or 'output')
            return response

    return render_to_response('webtools/xsams2sme.html',
            RequestContext(request,dict(conversion=ConvForm)))

