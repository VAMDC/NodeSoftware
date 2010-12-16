# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf import settings

def index(request):
    c=RequestContext(request,{})
    return render_to_response('vald/index.html', c)


