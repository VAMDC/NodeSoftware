# -*- coding: utf-8 -*-
# Create your views here.
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from DjBASECOL.bastest.models import RefsArticles,RefsGroups,Energytables,ELevels


def index(request):
    return HttpResponse("Hello, world. You're at the basecol index.")
    
def authors(request, ref_id):
    rarts=RefsGroups.objects.select_related('article__journal','article__authors','article__adsnote').filter(pk=ref_id)
    resp="Titles:<br>"
    resp+="<UL>"
    for rag in rarts.all():
        rart=rag.article
        resp+="<li> %s in %s (%s)<ol>"%(rart.title,rart.journal.smallname,rart.adsnote.value)
        for raut in rart.authors.all():
            resp+="<li>%s %s" %(raut.surname,raut.firstname)
        resp+="</ol>"
    resp+="</UL>"
    return HttpResponse(resp)
    
def etable(request, ref_id):
    eta=Energytables.objects.select_related('symmelement__element','symmelement__symmetry').filter(pk=ref_id)
    resp="ETable:"
    for et in eta.all():
        resp+='<ul><li>%s'%et.title
        resp+='<br>el %s %s'%(et.symmelement.symmetry.designation,et.symmelement.element.designation)
        resp+='<br>levels<ol>'
        elevs=ELevels.objects.filter(idenergytable=ref_id)
        for elev in elevs.all():
            resp+='<li>level %s energy %s'%(elev.level,elev.energy)
        resp+='</ol></ul>'
    return HttpResponse(resp)
