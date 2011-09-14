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
    inurl = URLField(label='Input URL',required=False,widget=TextInput(attrs={'size': 50, 'title': 'Paste here a URL that delivers an XSAMS document.',}))

    def clean(self):
        infile = self.cleaned_data.get('infile')
        inurl = self.cleaned_data.get('inurl')
        if (infile and inurl) or (not (infile or inurl)):
            raise ValidationError('Give either input file or URL!')

        return self.cleaned_data

def transform(data):
    try: xml=e.parse(data)
    except Exception,err:
        raise ValidationError('Could not parse XML file: %s'%err)
    try: return xsl(xml)
    except Exception,err:
        raise ValidationError('Could not transform XML file: %s'%err)

def xsams2sme(request):
    if request.method != 'POST':
        ConvForm = ConversionForm()
    else:
        ConvForm = ConversionForm(request.POST, request.FILES)
        if ConvForm.is_valid():
            infile=ConvForm.cleaned_data.get('infile')
            inurl=ConvForm.cleaned_data.get('inurl')
            if infile:
                data = transform(infile)
            elif inurl:
                try: data = urlopen(inurl)
                except Exception,err:
                    raise ValidationError('Could not open given URL: %s'%err)
                data = transform(data)
            response=HttpResponse(data,mimetype='text/csv')
            response['Content-Disposition'] = \
                'attachment; filename=%s.sme'% (getattr(infile, 'name', None) or 'output')
            return response

    return render_to_response('webtools/xsams2sme.html',
            RequestContext(request,dict(conversion=ConvForm)))

