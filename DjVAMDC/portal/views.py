from django.shortcuts import render_to_response,get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

# from DjVAMDC.node.models import SomeModel

def index(request):
    c=RequestContext(request,{})
    return render_to_response('portal/index.html', c)

def query(request):
    c=RequestContext(request,{})
    return render_to_response('portal/index.html', c)
