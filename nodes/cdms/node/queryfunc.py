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



def Wavelength2MHz(op, foo):
    """
    Replace the query clause "Wavelength <op> <foo>" with
    "Frequency <op'> <foo'>", making the conversion from Angstroms to
    MHz.
    
    """
    
    if op == 'in':
        print 'Sorry - "in" queries not yet implemented for RadTransWavelength'
        return None
    
    opp = op
    if op == '<':
        opp = '>'
    if op == '<=' or op == '=<':
        opp = '>='
    if op == '>':
        opp = '<'
    if op == '>=' or op == '=>':
        opp = '<='
    try:
        foop = float(foo[0])
    except (ValueError, TypeError):
        print 'failed to convert %s to float' % foo
        return None
    except (IndexError):
        print 'no argument to Wavelength restrictable'
        return None
    if foop != 0.:
        # Angstroms -> cm-1
        foop = 2.99792458e12 / foop
    else:
        # zero wavelength requested, so set frequency to something huge
        foop = 1.e20
    q = ['RadTransFrequency', opp, str(foop)]
    return q





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
#    q = sql2Q(sql)

    # sql2Q(sql) - code copied as c.hill did for the hitran-node
    logic, rs, count = splitWhere(sql.where)
    # and replace any restrictions on ChemicalName or StoichiometricFormula
    # with the equivalent on MoleculeInchiKey. Also convert wavelength
    # (in A) to wavenumber:
    for i in rs:
        r, op, foo = rs[i][0], rs[i][1], rs[i][2:]
    #    if r == 'MoleculeChemicalName':
    #        rs[i] = ChemicalName2MoleculeInchiKey(op, foo)
    #    if r == 'MoleculeStoichiometricFormula':
    #        rs[i] = StoichiometricFormula2MoleculeInchiKey(op, foo)
        if r == 'RadTransWavelength':
            rs[i] = Wavelength2MHz(op, foo)
    qdict = restriction2Q(rs)
    q = mergeQwithLogic(qdict, logic)

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

    # ADD additional restricables for this output method which are
    # only meaningful for CDMS
    #RESTRICTABLES['dataset']='dataset'
    RESTRICTABLES.update(CDMSONLYRESTRICTABLES)

    if tap.format != 'spcat' and tap.format!='png':
        emsg = 'Currently, only FORMATs PNG, SPCAT and XSAMS are supported.\n'
        return tapServerError(status=400, errmsg=emsg)

    # XXX more duplication of code from setupResults():
    # which uses sql = tap.parsedSQL
#    q = where2q(tap.parsedSQL.where, RESTRICTABLES)
#    q = sql2Q(tap.parsedSQL)
    # sql2Q(sql) - code copied as c.hill did for the hitran-node
    logic, rs, count = splitWhere(tap.parsedSQL.where)
    # and replace any restrictions on ChemicalName or StoichiometricFormula
    # with the equivalent on MoleculeInchiKey. Also convert wavelength
    # (in A) to wavenumber:

    for i in rs:
        r, op, foo = rs[i][0], rs[i][1], rs[i][2:]
    #    if r == 'MoleculeChemicalName':
    #        rs[i] = ChemicalName2MoleculeInchiKey(op, foo)
    #    if r == 'MoleculeStoichiometricFormula':
    #        rs[i] = StoichiometricFormula2MoleculeInchiKey(op, foo)
        if r == 'RadTransWavelength':
            rs[i] = Wavelength2MHz(op, foo)

        
    qdict = restriction2Q(rs)
    q = mergeQwithLogic(qdict, logic)


    # use tap.parsedSQL.columns instead of tap.requestables
    # because only the selected columns should be returned and no additional ones
    col = tap.parsedSQL.columns #.asList()

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
    transs = TransitionsCalc.objects.filter(q,species__origin=5,dataset__archiveflag=0).order_by('frequency') 
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
#    if ('radiativetransitions' in tap.requestables):
        LOG('TRANSITIONS')
        transitions = transs
    else:
        LOG('NO TRANSITIONS')
        transitions = []

        
    if (col=='ALL' or 'states' in [x.lower() for x in col] ):
#    if ('states' in tap.requestables ):
        LOG('STATES')
        states = States.objects.filter(q,species__origin=5,dataset__archiveflag=0)
    else:
        LOG('NO STATES')
        states = []
        
    if tap.format=='spcat':
        generator = gener(transitions, states)
        response = HttpResponse(generator, mimetype='text/plain')
    else:
        if 'states' in tap.requestables:
            response = plotLevelDiagram(states)
        else:
            response = plotStickSpec(transitions)
        
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


def plotStickSpec(transs):
    import os
    os.environ['HOME']='/tmp'

    
    import matplotlib
    from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
    from matplotlib.figure import Figure
    from matplotlib.dates import DateFormatter
    fig = Figure(facecolor='#eeefff',figsize=(15, 10), dpi=80,edgecolor='w')
    
    ax=fig.add_subplot(1,1,1)
    # bx=fig.add_subplot(2,1,1)


    spids = set( transs.values_list('species_id',flat=True) )
    spidsname = []
    species = Species.objects.filter(pk__in=spids) #,ncomp__gt=1)
    i=0
    bars=[]
    for specie in species:
        spidsname.append(specie.name)
        subtranss = transs.filter(species=specie)
        intensities = [10.0**trans.intensity for trans in subtranss]
        frequencies = [trans.frequency for trans in subtranss]
        #bars.append( ax.bar(frequencies, intensities, color=cm.jet(1.*i/len(spids)))[0] )
        bars.append( ax.bar(frequencies, intensities, linewidth=1,edgecolor=matplotlib.cm.jet(1.*i/len(spids)), color=matplotlib.cm.jet(1.*i/len(spids)))[0] )
        i=i+1
        
 
    ax.legend(bars,spidsname,loc=0)
#    intensities = [10.0**trans.intensity for trans in transs]
#    frequencies = [trans.frequency for trans in transs]
# #   #IDs = [trans.species for trans in transs]

#    ax.bar(frequencies, intensities) #, color=cols)
    
    ax.set_xlabel("Frequency [MHz]")
    ax.set_ylabel("Intensity [nm^2MHz]")

    title = u"Dynamically Generated Stick Spectrum "
    ax.set_title(title)


    ax.grid(True)
    canvas = FigureCanvas(fig)
    response = HttpResponse(content_type='image/png')
    
    canvas.print_png(response)
    return response



def plotLevelDiagram(states):
    import os
    os.environ['HOME']='/tmp'

    
    import matplotlib
    from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
    from matplotlib.figure import Figure
    from matplotlib.dates import DateFormatter
    fig = Figure(facecolor='#eeefff',figsize=(15, 10), dpi=80,edgecolor='w')
    
    ax=fig.add_subplot(1,1,1)
    # bx=fig.add_subplot(2,1,1)
        
    ax.set_xlabel("J")
    ax.set_ylabel("Energy [cm-1]")


    spids = set( states.values_list('species_id',flat=True) )
    spidsname = []
    species = Species.objects.filter(pk__in=spids) #,ncomp__gt=1)
    i=0
    plots=[]
    for specie in species:
        spidsname.append(specie.name)
        substates = states.filter(species=specie)

        for state in states:
            pl = ax.plot([state.qn1-0.3,state.qn1+0.3],[state.energy,state.energy], color=matplotlib.cm.jet(1.*i/len(spids)))

        plots.append(pl)
        i=i+1
        
    ax.legend(plots, spidsname, loc=0)
#    ax.legend(bars,spidsname,loc=0)
    

#    for state in states:
#        ax.plot([state.qn1-0.3,state.qn1+0.3],[state.energy,state.energy], color='b')
 
    
    title = u"Energy Level Diagram "
    ax.set_title(title)


    ax.grid(True)
    canvas = FigureCanvas(fig)
    response = HttpResponse(content_type='image/png')
    
    canvas.print_png(response)
    return response
