# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse, QueryDict

from models import *
from searchform import *

# work out which molecules are present in the database ...
loaded_molecules = Trans.objects.values('molecid').distinct()
# ... and get their names and html-names from the molecules table:
molecules = Molecules.objects.filter(molecid__in=loaded_molecules).values(
        'molecid','molec_name','molec_name_html')
# Do the same for molecules with cross sections in the HITRAN database:
xsec_molecules = Molecules.objects.filter(molecid__in=Xsec.objects.values(
        'molecid').distinct()).values('molecid','molec_name','molec_name_html')
# make the HTML for the molecule checkboxes:
molec_cb_html_soup = ['<table>\n']
i = 0
for molecule in molecules:
    if not i % 4: molec_cb_html_soup.append('<tr>')
    molec_cb_html_soup.append('<td><input type="checkbox"' \
        ' name="molecule" value="%d"/>&nbsp;%s</td>'
        % (molecule['molecid'], molecule['molec_name_html']))
    if i%4 == 3: molec_cb_html_soup.append('</tr>\n')
    i += 1
molec_cb_html_soup.append('</table>\n')
molec_cb_html = ''.join(molec_cb_html_soup)

def index(request):
    if request.POST:
        form = SearchForm(request.POST)
        if form.is_valid():
            req = make_request(form)
            search_summary = process_request(req)
            return render_to_response('search_results.html', search_summary)
        else:
            return  HttpResponse('Bad Form, old boy!')
        
    c=RequestContext(request,{})


    return render_to_response('index.html',
        {'molec_cb_html': molec_cb_html, })

