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
        if (infile and inurl):
            raise ValidationError('Give either input file or URL!')

        if inurl:
            try: data = urlopen(inurl)
            except Exception,err:
                raise ValidationError('Could not open given URL: %s'%err)
        elif infile: data = infile
        else:
            raise ValidationError('Give either input file or URL!')

        try: xml=e.parse(data)
        except Exception,err:
            raise ValidationError('Could not parse XML file: %s'%err)
        try: self.cleaned_data['sme'] = xsl(xml)
        except Exception,err:
            raise ValidationError('Could not transform XML file: %s'%err)

        return self.cleaned_data

def xsams2sme(request):
    if request.method != 'POST':
        ConvForm = ConversionForm()
    else:
        ConvForm = ConversionForm(request.POST, request.FILES)
        if ConvForm.is_valid():
            response=HttpResponse(ConvForm.cleaned_data['sme'],mimetype='text/csv')
            response['Content-Disposition'] = \
                'attachment; filename=%s.sme'% (ConvForm.cleaned_data.get('infile') or 'output')
            return response

    return render_to_response('webtools/xsams2sme.html',
            RequestContext(request,dict(conversion=ConvForm)))

