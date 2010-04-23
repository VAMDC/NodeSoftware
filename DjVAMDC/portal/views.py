from django.shortcuts import render_to_response,get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django import forms

# from DjVAMDC.node.models import SomeModel

def index(request):
    c=RequestContext(request,{})
    return render_to_response('portal/index.html', c)

class QueryForm(forms.Form):
    sql=forms.CharField()

def query(request):
    if request.method == 'POST': # If the form has been submitted...
        form = QueryForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            # ...
            return HttpResponseRedirect('http://vamdc.fysast.uu.se:8888/node/vald/tap/sync/?REQUEST=doQuery&LANG=ADQL&FORMAT=XSAMS&QUERY=SELECT%20ALL%20WHERE%20WAVELENGTH%20%3E%203000%20AND%20WAVELENGTH%20%3C%203500%20AND%20ELEMENT%20=%20Fe',) # Redirect after POST
    else:
        form = QueryForm() # An unbound form

    return render_to_response('portal/query.html', {
                                                    'form': form,
                                                    })
