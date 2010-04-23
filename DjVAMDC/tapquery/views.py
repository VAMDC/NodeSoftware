from django.shortcuts import render_to_response,get_object_or_404
from django.db.models import Q
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

def index(request):
    c=RequestContext(request,{})
    return render_to_response('tapservice/index.html', c)

