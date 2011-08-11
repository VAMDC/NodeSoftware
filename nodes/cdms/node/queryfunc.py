# -*- coding: utf-8 -*-
from django.db.models import Q
from django.conf import settings
import sys
def LOG(s):
    if settings.DEBUG: print >> sys.stderr, s

from dictionaries import *
from itertools import chain
from copy import deepcopy

from models import *
from vamdctap.sqlparse import *

from django.template import Context, loader
from django.http import HttpResponse
def tapServerError(request=None, status=500, errmsg=''):
    text = 'Error in TAP service: %s' % errmsg
    # XXX I've had to copy TAP-error-document.xml into my node's
    # template directory to get access to it, as well...
    document = loader.get_template('tap/TAP-error-document.xml').render(
                     Context({"error_message_text" : text}))
    return HttpResponse(document, status=status, mimetype='text/xml');
                                

if hasattr(settings,'TRANSLIM'):
    TRANSLIM = settings.TRANSLIM
else: TRANSLIM = 5000

#def getRefs(transs):
#    llids=set()
#    for t in transs.values_list('wave_ref_id','loggf_ref_id','lande_ref_id','gammarad_ref_id','gammastark_ref_id','waals_ref'):
#        llids = llids.union(t)
#    lls=LineList.objects.filter(pk__in=llids)
#    rids=set()
#    for ll in lls:
#        rids=rids.union(ll.references.values_list('pk',flat=True))
#    return Reference.objects.filter(pk__in=rids)

def attach_state_qns(states):
    for state in states:
        state.parsed_qns = []
        qns = MolecularQuantumNumbers.objects.filter(statesmolecules=state.stateid)
#        for qn in qns.order_by('id'):
        for qn in qns:
            if qn.attribute:
                # put quotes around the value of the attribute
                attr_name, attr_val = qn.attribute.split('=')
                qn.attribute = '%s="%s"' % (attr_name, attr_val)
 #           if qn.spinref:
                # add spinRef to attribute if it exists
#                qn.attribute += ' spinRef="%s"' % qn.spinref
            state.parsed_qns.append(MolecularQuantumNumbers(qn.stateid, qn.case, qn.label, qn.value, qn.attribute)) #, qn.xml))

def attach_partionfunc(molecules):
    for molecule in molecules:
        molecule.partionfuncT = []
        molecule.partionfuncQ = []
        
        pfs = Partitionfunctions.objects.filter(eid = molecule.id)
        
        temp=pfs.values_list('temperature',flat=True)
        pf = pfs.values_list('partitionfunc',flat=True)
                   
        molecule.partitionfuncT=temp
        molecule.partitionfuncQ=pf
         

def getSpeciesWithStates(transs):
#    LOG("speciesList:")
    spids = set( transs.values_list('species_id',flat=True) )
#    LOG(spids)
#    atoms = Species.objects.filter(pk__in=spids,ncomp=1)
    molecules = Species.objects.filter(pk__in=spids) #,ncomp__gt=1)
#    nspecies = atoms.count() + molecules.count()
    nspecies = molecules.count()
    nstates = 0
#    for species in [atoms,molecules]:
#    for species in [molecules]:  
    for specie in molecules:
            subtranss = transs.filter(species=specie)
            up=subtranss.values_list('upperstateref',flat=True)
            lo=subtranss.values_list('lowerstateref',flat=True)
            sids = set(chain(up,lo))
            specie.States = States.objects.filter( pk__in = sids)
            nstates += len(sids)
#            attach_state_qns(specie.States)


#    return atoms,molecules,nspecies,nstates
    return molecules,nspecies,nstates

def getFreqMethodRefs(transs):
    ids=set([5])  # the only one for now
#    for trans in transs:
#      ids=ids.union(set([trans.freqmethodref_id]))
    q=Q(id__in=ids)
    return Methods.objects.filter(q)

def getSources(transs):
#    ids=set([])
    meth=[]
#    for trans in transs:
#      ids=ids.union(set([trans.speciesid]))

    ids = set( transs.values_list('species_id',flat=True) )
      
    q=Q(eId__in=ids)

    slist = SourcesIDRefs.objects.filter(q).distinct()  
    for src in slist.values_list('eId',flat=True):
        mesrc=SourcesIDRefs.objects.filter(Q(eId=src)).values_list('rId',flat=True)
#        LOG(mesrc)
        this_method = Method(src,src,'derived','derived with Herb Pickett\'s spfit / spcat fitting routines, based on experimental data',mesrc)
#        meth=meth.append(Method(5,src,'derived','derived',mesrc))
#        LOG(this_method.sourcesref)
        meth.append(this_method)
#        LOG(meth)

        
    sourceids = slist.values_list('rId',flat=True)

    return Sources.objects.filter(pk__in = sourceids), meth
    



def setupResults(sql):
    LOG(sql)
    q=where2q(sql.where,RESTRICTABLES)
    try: q=eval(q)
    except: return {}

    LOG(q)
    transs = TransitionsCalc.objects.filter(q,species__origin=5,dataset__archiveflag=0) #order_by('vacwave')
#    transs = RadiativeTransitions.objects.select_related(depth=2).filter(q)
    
#    ntranss=transs.count()
  #  if TRANSLIM < ntranss :
  #      percentage='%.1f'%(float(TRANSLIM)/ntranss *100)
  #      newmax=transs = transs[TRANSLIM].vacwave
  #      transs=Transition.objects.filter(q,Q(vacwave__lt=newmax))
  #  else: percentage=None
    percentage=None
    ntranss=transs.count()
    LOG(ntranss)
#    sources = getRefs(transs)
    sources, methods = getSources(transs)
    nsources = sources.count()
#    atoms,molecules,nspecies,nstates = getSpeciesWithStates(transs)
    LOG(nsources)
    molecules,nspecies,nstates = getSpeciesWithStates(transs)
    LOG(nspecies)
    LOG(nstates)
    attach_partionfunc(molecules)
    
#    LOG(ntranss)
#    LOG(methods)
    headerinfo={\
            'Truncated':percentage,
 #           'COUNT-SOURCES':nsources,
            'COUNT-species':nspecies,
            'count-states':nstates,
            'count-radiative':ntranss
            }

#    methods = [Method('MOBS', 'observed', 'observed'),
#                   Method('MDER', 'derived', 'derived')]
                   
#    methods = getFreqMethodRefs(transs)

    return {'RadTrans':transs,
  #          'Atoms':atoms,
            'Molecules':molecules,
            'Sources':sources,
            'Methods':methods,
            'HeaderInfo':headerinfo,
  #          'Environments':Environments #this is set up statically in models.py
           }



def returnResults(tap, LIMIT=None):
    """
    Return this node's response to the TAP query, tap, where
    the requested return format is something other than XSAMS.
    The TAP object has been validated upstream of this method,
    so we're good to go.

    """

    if tap.format != 'spcat':
        emsg = 'Currently, only FORMATs SPCAT and XSAMS are supported.\n'
        return tapServerError(status=400, errmsg=emsg)

    # XXX more duplication of code from setupResults():
    # which uses sql = tap.parsedSQL
    q = where2q(tap.parsedSQL.where, RESTRICTABLES)
    LOG(tap.parsedSQL.columns)
    col = tap.parsedSQL.columns #.asList()
    LOG(q)
    try:
        q=eval(q)
    except Exception,e:
        LOG('Exception in setupResults():')
        LOG(e)
        return {}

    transs = TransitionsCalc.objects.filter(q,species__origin=5,dataset__archiveflag=0) 
    ntrans = transs.count()
    if LIMIT is not None and ntrans > LIMIT:
        # we need to filter transs again later, so can't take a slice
        #transs = transs[:LIMIT]
        # so do this:
        numax = transs[LIMIT].nu
        transs = TransitionsCalc.objects.filter(q, Q(nu__lte=numax))
        percentage = '%.1f' % (float(LIMIT)/ntrans * 100)
    else:
        percentage = '100'
#    print 'Truncated to %s %%' % percentage
    transs = TransitionsCalc.objects.filter(q,species__origin=5,dataset__archiveflag=0) 
    ntrans = transs.count()
    if LIMIT is not None and ntrans > LIMIT:
        # we need to filter transs again later, so can't take a slice
        #transs = transs[:LIMIT]
        # so do this:
        numax = transs[LIMIT].nu
        transs = TransitionsCalc.objects.filter(q, Q(nu__lte=numax))
        percentage = '%.1f' % (float(LIMIT)/ntrans * 100)
    else:
        percentage = '100'
#    print 'Truncated to %s %%' % percentage
#    print 'ntrans =',ntrans


#    if 'radiativetransitions' in col:
#        cat_generator = Cat(transs)
#    else:
#        LOG(col[0])
#        cat_generator = Cat(transs)
#        states = States.objects.filter(q,species__origin=5,dataset__archiveflag=0)
#        egy_generator = gener(transs, states)
#        cat_generator=egy_generator
#        cat_generator = ''



    if (col=='ALL' or 'radiativetransitions' in [x.lower() for x in col]):
        LOG('TRANSITIONS')
        transitions = transs
    else:
        LOG('NO TRANSITIONS')
        transitions = []

    if (col=='ALL' or 'states' in [x.lower() for x in col] ):
        LOG('STATES')
        states = States.objects.filter(q,species__origin=5,dataset__archiveflag=0)
    else:
        LOG('NO STATES')
        states = []
        

    generator = gener(transitions, states)
    response = HttpResponse(generator, mimetype='text/plain')
        
    return response

def GetStringValue(value):
    if value == None: 
        return ''
    else:
        return value

def GetNumericValue(value):
    if value == None: 
        return 0
    else:
        return value
    

def gener(transs=None, states=None):
    for trans in Cat(transs):
        yield trans
    for state in Egy(states):
        yield state
        
    

def Cat(transs):
    for trans in transs:
        yield '%16.4lf' % trans.frequency
        yield '%8.4lf' % trans.uncertainty
        yield '%8.4lf' % trans.intensity
        yield '%2d' % trans.degreeoffreedom
        yield '%10.4lf' % trans.energylower

        yield '%3d' % trans.upperstatedegeneracy
        yield '%7d' % trans.speciestag
        
        yield '%7d' % trans.qntag
        yield '%2s' % GetStringValue(trans.qnup1)
        yield '%2s' % GetStringValue(trans.qnup2)
        yield '%2s' % GetStringValue(trans.qnup3)
        yield '%2s' % GetStringValue(trans.qnup4)
        yield '%2s' % GetStringValue(trans.qnup5)
        yield '%2s' % GetStringValue(trans.qnup6)

        yield '%2s' % GetStringValue(trans.qnlow1)
        yield '%2s' % GetStringValue(trans.qnlow2)
        yield '%2s' % GetStringValue(trans.qnlow3)
        yield '%2s' % GetStringValue(trans.qnlow4)
        yield '%2s' % GetStringValue(trans.qnlow5)
        yield '%2s' % GetStringValue(trans.qnlow6)

        yield '%s' % trans.species.name
        yield '\n'


def Egy(states):
    for state in states:
        yield '%5s' % GetStringValue(state.block)
        yield '%5s' % GetStringValue(state.index)                
        yield '%18.6lf' % GetNumericValue(state.energy)
        yield '%18.6lf' % GetNumericValue(state.mixingcoeff)
        yield '%18.6lf' % GetNumericValue(state.uncertainty)

        yield '%3s' % GetStringValue(state.qn1)
        yield '%3s' % GetStringValue(state.qn2)
        yield '%3s' % GetStringValue(state.qn3)
        yield '%3s' % GetStringValue(state.qn4)
        yield '%3s' % GetStringValue(state.qn5)
        yield '%3s' % GetStringValue(state.qn6)

        yield '%s' % GetStringValue(state.species.name)
        yield '%3s' % GetStringValue(state.degeneracy)          
        yield '%4s' % GetStringValue(state.nuclearspinisomer)
        yield '%7s' % GetStringValue(state.nuclearstatisticalweight)
        yield '%4s ' % GetStringValue(state.qntag)

        yield '\n'
