# -*- coding: utf-8 -*-

# This is where you would add additional functionality to your node, 
# bound to certain URLs in urls.py

from django.conf import settings
from django.http import HttpResponse
from django.template import Context, Template
from django.template.loader import get_template
from django.shortcuts import render, get_object_or_404

import node.models as models# this imports models.py from the same directory as this file

from django.db.models import Q

# this function fetches energyscan data from the db and is defined as a function
# because it is needed several times throughout this file

def get_ES_from_db(id):
    """ Grab energyscan data from database """
    energyscan = get_object_or_404(models.Energyscan, pk=id)
    ES_list = energyscan.energyscan_data.split()
    k = 0
    xs = []
    ys = []
    for datapoint in ES_list:
        datapoint = datapoint.replace(',','.')
        #even -> x-value
        if k % 2 == 0:
            xs.append(float(datapoint))
        #odd -> y-value
        else:
            ys.append(float(datapoint))
        k = k + 1

    #we end at this point, because the further handling of the data depends on the function

    return energyscan, xs, ys

def show_energyscan(request, id):
    """ Fill the normal template to show ES on the webinterface """
    # get data from db
    energyscan, xs, ys = get_ES_from_db(id)
    xs = list(map(str, xs))
    ys = list(map(str, ys))
    k = 0
    stringarray = []
    for x in xs:
        stringarray.append('[%s, %s]'%(x, ys[k]))
        k = k + 1

    energyscan.daten = " ,".join(stringarray)

    #sources:
    authorlist = []
    source = models.Source.objects.filter(id__exact=energyscan.source.id).get()
    for author in source.authors.all():
        authorlist.append(u'%s, %s'%(author.lastname, author.firstname))

    energyscan.authorlist = "; ".join(authorlist)

    t = 'node/energyscan_view.html'
    c = {'es':energyscan}
    return HttpResponse(render(request, t, c))

def compare_energyscan(request, id1, id2):
    """ Compare two ES on the webinterface """
    # get data from db
    energyscan1, xs1, ys1 = get_ES_from_db(id1)
    energyscan2, xs2, ys2 = get_ES_from_db(id2)

    stringarray1 = []
    stringarray2 = []

    #compare scans - multiply items of second with factor between max(1) and max(2)
    factor = max(ys1) / max(ys2)
    ys2[:] = [x*factor for x in ys2]
    energyscan2.factor = "%.2f" % factor

    #prepare scan1 for text-format

    xs1 = list(map(str, xs1))
    ys1 = list(map(str, ys1))
    k = 0
    for x in xs1:
        stringarray1.append('[%s, %s]'%(x, ys1[k]))
        k = k + 1

    energyscan1.daten = " ,".join(stringarray1)

    #prepare scan2 for text-format

    xs2 = list(map(str, xs2))
    ys2 = list(map(str, ys2))
    k = 0
    for x in xs2:
        stringarray2.append('[%s, %s]'%(x, ys2[k]))
        k = k + 1

    energyscan2.daten = " ,".join(stringarray2)

    #sources:
    authorlist = []
    source = models.Source.objects.filter(id__exact=energyscan1.source.id).get()
    for author in source.authors.all():
        authorlist.append(u'%s, %s'%(author.lastname, author.firstname))

    energyscan1.authorlist = "; ".join(authorlist)

    authorlist = []
    source = models.Source.objects.filter(id__exact=energyscan2.source.id).get()
    for author in source.authors.all():
        authorlist.append(u'%s, %s'%(author.lastname, author.firstname))

    energyscan2.authorlist = "; ".join(authorlist)


    #render and return

    t = 'node/energyscan_compare.html'
    c = {'es1':energyscan1, 'es2':energyscan2}
    html = render(request, t, c)
    return HttpResponse(html)

def contact(request):
    contactdetails = {'name':'Johannes Postler', 'email':'johannes.postler@uibk.ac.at'}
    t = 'node/contact.html'
    c = {'contact':contactdetails}
    html = render(request, t, c)
    return HttpResponse(html)

def export_ascii(request, id):
    """ Export ES to ASCII file """
    #get data from db
    energyscan, xs, ys = get_ES_from_db(id)
    
    stringarray = []
    k = 0
    for x in xs:
        stringarray.append('%f\t%f'%(x, ys[k]))
        k = k + 1

    energyscan.daten = "\r\n".join(stringarray)

    t = 'node/ascii_export.txt'
    c = {'es':energyscan}
    filename = "ES_" + str(energyscan.species) + "_from_" + str(energyscan.origin_species) + ".txt"
    html = render(request, t, c)
    resp = HttpResponse(html, content_type='text/plain')
    resp['Content-Disposition'] = 'attachment; filename=%s' % filename
    return resp
