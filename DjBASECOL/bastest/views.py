# -*- coding: utf-8 -*-
# Create your views here.
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from DjBASECOL.bastest.models import RefsArticles,RefsGroups,ETables,Elements


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

def getBASECOLSources(states):
    ris=[]
    for se in states.all():
        for syme in se.symmels.all():
          for et in syme.etables.all():
              ris.append(et.idrefgroup)
      #refids = [obj.symmels.all().etables.all().idrefgroup for obj in states.all()]
    #rarts=RefsGroups.objects.select_related('article__journal','article__authors','article__adsnote').filter(pk=1121)
    return RefsGroups.objects.select_related('article__journal','article__authors','article__adsnote').filter(pk__in= ris)
    #return rarts

def getBASECOLStates():
    return Elements.objects.select_related(depth=4).filter(pk=34)

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


#
#   "TAP implementation :)"
#   let's have some sources
#

def setupResults(tap,limit=0):
    
    states = getBASECOLStates()
    sources = getBASECOLSources(states)
    #if tap.lang=='vamdc':
        #tap.query=tap.query%VALD_DICT
        #print tap.query
        ##transs = Transition.objects.extra(tables=['species','states'],where=[tap.query,'(transitions.lostate=states.id OR transitions.upstate=states.id)','transitions.species=species.id'],).order_by('airwave')
        #qtup=vamdc2queryset(tap.query)
        #transs = Transition.objects.filter(*qtup).order_by('airwave')
    #else:
        #qtup=parseSQL(tap.query)
        #transs = Transition.objects.filter(*qtup).order_by('airwave')
    
    #totalcount=transs.count()
    #if limit :
        #transs = transs[:limit]

    #sources = getVALDsources(transs)
    #states = getVALDstates(transs)
    #if limit:
        #return transs,states,sources,totalcount
    #else:
        #return transs,states,sources
    return {\
    
    'Sources':sources,
    'MoleStates':states
    }
