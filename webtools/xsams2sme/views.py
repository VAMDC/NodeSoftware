# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response,get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django import forms
from django.forms.formsets import formset_factory


def xsams2sme(request):
    c=RequestContext(request,{})
    return render_to_response('portal/index.html', c)

