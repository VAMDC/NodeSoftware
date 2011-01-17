# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse, QueryDict

from models import *

def index(request):
    c=RequestContext(request,{})

    return render_to_response('index.html', c)
