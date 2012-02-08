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


def attach_partionfunc(molecules):
    """
    Attaches partition functions to each specie.
    """
    for molecule in molecules:
        molecule.partionfuncT = []
        molecule.partionfuncQ = []
        
        #pfs = Partitionfunctions.objects.filter(eid = molecule.id, mid__isnull=False)
        pfs = Partitionfunctions.objects.filter(specie = molecule, state="All")
        
        temp=pfs.values_list('temperature',flat=True)
        pf = pfs.values_list('partitionfunc',flat=True)
                   
        molecule.partitionfuncT=temp
        molecule.partitionfuncQ=pf
         


def get_species_and_states(transs, addStates=True):
    """
    Returns list of species including all states which occur in the list
    of transitions.
    Returns:
    - Atoms
    - Molecules
    - Number of species
    - Number of states
    """

    spids = set( transs.values_list('specie_id',flat=True).distinct() )
    # Species object for CDMS includes Atoms AND Molecules. Both can only
    # be distinguished through numberofatoms-field
    atoms = Species.objects.filter(pk__in=spids, molecule__numberofatoms__exact='Atomic')
    molecules = Species.objects.filter(pk__in=spids).exclude(molecule__numberofatoms__exact='Atomic') #,ncomp__gt=1)
    # Calculate number of species in total
    nspecies = atoms.count() + molecules.count()
    # Intialize state-counter
    nstates = 0

    if addStates:
        # Loop through list of species and attach states
        for specie in chain(atoms , molecules):
            # Get distinct list of States which
            # occur as lower or upper state in transitions
            subtranss = transs.filter(specie=specie)
            up=subtranss.values_list('upperstateref',flat=True)
            lo=subtranss.values_list('lowerstateref',flat=True)
            sids = set(chain(up,lo))
            # Attach states to species object
            specie.States = States.objects.filter( pk__in = sids)
            # Add number of attached states to state-counter
            nstates += specie.States.count()

    return atoms,molecules,nspecies,nstates



def get_sources(transs, methods = []):
    """
    Get a complete list of sources and methods for the set of
    predicted transitions. Methods compiled for observed
    transitions have to be transfered via input variable method in
    order to be included in the output.
    """

    # Get the list of species (entries). One method is generated for each specie
    ids = set( transs.values_list('specie_id',flat=True) )
    slist = SourcesIDRefs.objects.filter(specie__in=ids).distinct()

    sexplist = slist.filter(transitionexp__gt=0)

    # Loop over species list and get sources
    for src in slist.values_list('specie',flat=True):
        mesrc=SourcesIDRefs.objects.filter(Q(specie=src)).distinct().values_list('source',flat=True)
        this_method = Method(src,src,'derived','derived with Herb Pickett\'s spfit / spcat fitting routines, based on experimental data',mesrc)
        methods.append(this_method)

    # Loop over species list and get sources
    for src in sexplist.values_list('source',flat=True):
        this_method =  Method('EXP'+str(src),src,'experimental','experimental',src)
        methods.append(this_method)
        
    sourceids = slist.values_list('source',flat=True)

    return Sources.objects.filter(pk__in = sourceids), methods
    


def attach_exp_frequencies(transs):
    """
    Create lists of frequencies, units, sources, ... for each transition.
    The calculated frequency is given anyway followed by experimental
    frequencies (db-table: Frequencies). In addition a unique list of
    methods for the experimental data is created and returned.

    Returns:
    - modified transitions (frequencies, ... attached as lists)
    - methods for experimental data
    
    """
    methodrefs = []
    methods = []
    
    # Loop over calculated transitions (Predictions)
    # and attach Experimental Frequencies
    for trans in transs:
        
        # Attach the calculated frequency first
        trans.frequencies=[trans.frequency]
        trans.units=[trans.unit]
        trans.uncertainties=[trans.uncertainty]
        trans.refs=[""]
        trans.methods=[trans.specie.id]
        
        exptranss = TransitionsExp.objects.filter(species=trans.species,
                                                  qnup1=trans.qnup1,
                                                  qnlow1=trans.qnlow1,
                                                  qnup2=trans.qnup2,
                                                  qnlow2=trans.qnlow2,
                                                  qnup3=trans.qnup3,
                                                  qnlow3=trans.qnlow3,
                                                  qnup4=trans.qnup4,
                                                  qnlow4=trans.qnlow4,
                                                  qnup5=trans.qnup5,
                                                  qnlow5=trans.qnlow5,
                                                  qnup6=trans.qnup6,
                                                  qnlow6=trans.qnlow6)
        
        for exptrans in exptranss:
            trans.frequencies.append(exptrans.frequency)
            trans.units.append(exptrans.unit)
            trans.uncertainties.append(exptrans.uncertainty)
            # get sources
            s= exptrans.sources.all().values_list('source',flat=True)
            trans.refs.append(s)

            method = "EXP" + "-".join(str(source) for source in s)
            trans.methods.append(method)
            methodrefs.append(method)

    # Create a distinct list of methods
    methodrefs = list(set(methodrefs))

    for ref in methodrefs:
        this_method =  Method(ref,None,'experimental','experimental',ref[3:].split("-"))
        methods.append(this_method)
        
    return transs, methods





def setupResults(sql):
    """
    This method queries the database with respect to the sql-query
    and compiles everything together for the vamdctap.generator function
    which is used to generate XSAMS - output.
    """
    q = sql2Q(sql)

    addStates = (not sql.requestables or 'atomstates' in sql.requestables or 'moleculestates' in sql.requestables)
    addTrans = (not sql.requestables or 'RadiativeTransitions' in sql.requestables)

    # Query the database and get calculated transitions (TransitionsCalc)
    transs = TransitionsCalc.objects.filter(q,specie__origin=5,
                                            specie__archiveflag=0,
                                            dataset__archiveflag=0) #.order_by('frequency')

    # Attach experimental transitions (TransitionsExp) to transitions
    # and obtain their methods. Do it only if transitions will be returned
    if addTrans:
        transs = transs.order_by('frequency')
        #transs, methods = attach_exp_frequencies(transs)
        methods=[]
    else:
        methods=[]
        
    # get sources and methods which have been used
    # to derive predicted transitions
    if addTrans:
        sources, methods = get_sources(transs, methods)
    else:
        sources=Sources.objects.none()

    # get atoms and molecules with states which occur in transition-block
    atoms, molecules,nspecies,nstates = get_species_and_states(transs, addStates)

    # attach partition functions to each specie
    attach_partionfunc(molecules)

    # this header info is used in xsams-header-info (html-request)
    headerinfo={\
        'Truncated':"0", # CDMS will not truncate data (at least for now)
        'count-sources':sources.count(),
        'count-species':nspecies,
        'count-molecules':molecules.count(),
        'count-atoms':atoms.count(),
        'count-states':nstates,
        'count-radiative':transs.count()
    }


    return {'RadTrans':transs,
            'Atoms':atoms,
            'Molecules':molecules,
            'Sources':sources,
            'Methods':methods,
            'HeaderInfo':headerinfo,
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
    RESTRICTABLES.update(CDMSONLYRESTRICTABLES)

    SUPPORTED_FORMATS=['spcat','png','list','xspcat','mrg']

    if tap.format not in SUPPORTED_FORMATS:
        emsg = 'Currently, only FORMATs PNG, SPCAT and XSAMS are supported.\n'
        return tapServerError(status=400, errmsg=emsg)

    if tap.format == 'list':
        speclist=specieslist()
        response = HttpResponse(speclist, mimetype='text/plain')
        return response
    LOG('And now some logs:')
    #LOG(tap.data)
        
    LOG(tap.parsedSQL)

#    for i in tap.parsedSQL:
#        if 'getonlycalc' in i:
#            LOG(i)
#        else:
#            psql.append(i)
#            LOG(i)
#        c+=1

    q = sql2Q(tap.parsedSQL)
    LOG(q)

    # use tap.parsedSQL.columns instead of tap.requestables
    # because only the selected columns should be returned and no additional ones
    col = tap.parsedSQL.columns #.asList()
    
    transs = TransitionsCalc.objects.filter(q,specie__origin=5,specie__archiveflag=0,dataset__archiveflag=0) 
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


    # Prepare Transitions
    if (col=='ALL' or 'radiativetransitions' in [x.lower() for x in col]):
        LOG('TRANSITIONS')
        orderby = tap.request.get('ORDERBY','frequency')
        if ',' in orderby:
            orderby=orderby.split(',')
            transitions = transs.order_by(*orderby) 
        else:            
            transitions = transs.order_by(orderby)
            
    else:
        LOG('NO TRANSITIONS')
        transitions = []


    # Prepare States if requested
    if (col=='ALL' or 'states' in [x.lower() for x in col] ):
        LOG('STATES')
        orderby = tap.request.get('ORDERBY','energy')
        states = States.objects.filter(q,specie__origin=5,dataset__archiveflag=0).order_by(orderby)
    else:
        LOG('NO STATES')
        states = []


    if tap.format in ('spcat','xspcat','mrg'):
        generator = gener(transitions, states, format=tap.format)
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
    
def formatqn(value):
    if value == None:
        return ''
    elif value > 99 and value < 360:
        return chr(55+value/10)+ "%01d" % ( value % 10)
    elif value < -9 and value > -260:
        return chr(95-(value-1)/10)+ "%01d" % -( value % -10)
    else:
        return str(value)

def gener(transs=None, states=None, format='spcat'):

    if format=='xspcat':
        for trans in xCat(transs):
            yield trans
    elif format == 'mrg':
        for trans in Mrg(transs):
            yield trans
    else:
        for trans in Cat(transs):
            yield trans
        for state in Egy(states):
            yield state
        

def Cat(transs):
    for trans in transs:
        yield '%13.4lf' % trans.frequency
        yield '%8.4lf' % trans.uncertainty
        yield '%8.4lf' % trans.intensity
        yield '%2d' % trans.degreeoffreedom
        yield '%10.4lf' % trans.energylower

        yield '%3d' % trans.upperstatedegeneracy
        yield '%7d' % trans.speciestag
        
        yield '%4d' % trans.qntag
        yield '%2s' % formatqn(trans.qnup1)
        yield '%2s' % formatqn(trans.qnup2)
        yield '%2s' % formatqn(trans.qnup3)
        yield '%2s' % formatqn(trans.qnup4)
        yield '%2s' % formatqn(trans.qnup5)
        yield '%2s' % formatqn(trans.qnup6)

        yield '%2s' % formatqn(trans.qnlow1)
        yield '%2s' % formatqn(trans.qnlow2)
        yield '%2s' % formatqn(trans.qnlow3)
        yield '%2s' % formatqn(trans.qnlow4)
        yield '%2s' % formatqn(trans.qnlow5)
        yield '%2s' % formatqn(trans.qnlow6)

        yield '%s' % trans.specie.name
        yield '\n'


def Mrg(transs):
    """
    """
    
    for trans in transs:
        trans.attach_exp_frequencies()

        speciestag = trans.speciestag

        if len(trans.frequencies)>1:
            speciestag=-speciestag
            frequency = trans.frequencies[1]
            uncertainty = trans.uncertainties[1]
        else:
            frequency = trans.frequency
            uncertainty = trans.uncertainty
            
        yield '%13.4lf' % frequency
        yield '%8.4lf' % uncertainty
        yield '%8.4lf' % trans.intensity
        
        yield '%2d' % trans.degreeoffreedom
        yield '%10.4lf' % trans.energylower

        yield '%3d' % trans.upperstatedegeneracy
        yield '%7d' % speciestag
        
        yield '%4d' % trans.qntag
        yield '%2s' % formatqn(trans.qnup1)
        yield '%2s' % formatqn(trans.qnup2)
        yield '%2s' % formatqn(trans.qnup3)
        yield '%2s' % formatqn(trans.qnup4)
        yield '%2s' % formatqn(trans.qnup5)
        yield '%2s' % formatqn(trans.qnup6)

        yield '%2s' % formatqn(trans.qnlow1)
        yield '%2s' % formatqn(trans.qnlow2)
        yield '%2s' % formatqn(trans.qnlow3)
        yield '%2s' % formatqn(trans.qnlow4)
        yield '%2s' % formatqn(trans.qnlow5)
        yield '%2s' % formatqn(trans.qnlow6)

        yield '%s' % trans.specie.name
        yield '\n'



def xCat(transs):
    # qnlabels = ["J","N","Ka","Kc","v"]
    qnlabels = []
    tagarray = transs.values_list('specie','qntag').distinct()
    for specie, qntag in tagarray:
        filter = QuantumNumbersFilter.objects.filter(specie= specie, qntag=qntag).order_by('order')
        qnlabels = chain(qnlabels, filter.values_list('label','order'))
    
#    qnlabels = set(qnlabels)
    qnlabels = sorted(set(qnlabels),key=lambda x:x[1])

#    statess = set( transs.values_list('upperstateref',flat=True) )

#    qns = MolecularQuantumNumbers.objects.filter(pk__in=statess).distinct()
#    dictqns = {}
#          
#          for qn in qns:
#               if qn.attribute:
#                    # put quotes around the value of the attribute
#                    attr_name, attr_val = qn.attribute.split('=')
#                    qn.attribute = ' %s="%s"' % (attr_name, attr_val)
#               else:
#                    qn.attribute = ''
#                    
#               if qn.spinref:
#                    # add spinRef to attribute if it exists
#                    qn.attribute += ' nuclearSpinRef="%s"' % qn.spinref

#               dictqns.update({qn.label : qn.value})


    # Header
    yield '%13s' % "Frequency"
    yield '%8s' % "Unc."
    yield '%8s' % "Intens."
    yield '%4s' % "DOF"
    yield '%12s' % "l. Energy."
    
    yield '%5s ' % "Gup"

    for qnlabel in qnlabels:
        yield '%4s' % qnlabel[0][:4]

    yield ' - '
    for qnlabel in qnlabels:
        yield '%4s' % qnlabel[0][:4]


    yield ' Specie'
    yield '\n'
    
    for trans in transs:
        yield '%13.4lf' % trans.frequency
        yield '%8.4lf' % trans.uncertainty
        yield '%8.4lf' % trans.intensity
        yield '%4d' % trans.degreeoffreedom
        yield '%12.4lf' % trans.energylower

        yield '%5d ' % trans.upperstatedegeneracy
#        yield '%7d' % trans.speciestag
        

        # Create quantum number output
        upperqns = trans.upperstateref.qns_dict()
        lowerqns = trans.lowerstateref.qns_dict()

#        yield '<div class="qn label">(%s) = </div>' % ",".join(upperqns)

        for label in qnlabels:
            if label[0]=='ElecStateLabel':
                val = str(upperqns.get(label[0]))[:1]
            else:
                val = str(upperqns.get(label[0]))

            if val=="None":
                val=""
                
            yield '<div class="qn %s">%4s</div>' % (label[0], val)

#        yield " <- "
        yield '   '

        for label in qnlabels:
            if label[0]=='ElecStateLabel':
                val = str(lowerqns.get(label[0]))[:1]
            else:
                val = str(lowerqns.get(label[0]))

            if  val=="None":
                val=""
                
            yield '<div class="qn %s">%4s</div>' % (label[0], val)
            

        yield ' %s' % trans.specie.name

        
        yield '\n'

        # QUERY and Display Experimental values
        exptranss = TransitionsExp.objects.filter(specie=trans.specie,
                                            qnup1=trans.qnup1,
                                            qnlow1=trans.qnlow1,
                                            qnup2=trans.qnup2,
                                            qnlow2=trans.qnlow2,
                                            qnup3=trans.qnup3,
                                            qnlow4=trans.qnlow4,
                                            qnup5=trans.qnup5,
                                            qnlow6=trans.qnlow6)
        for exptrans in exptranss:
            yield '<small style="color:blue">'
            yield '    %16.4lf' % exptrans.frequency
            yield '    %10.4lf' % exptrans.uncertainty
#            if exptrans.comment:
#            yield '    %20s' % (exptrans.comment if exptrans.comment else "")

            yield '   '
            sources = SourcesIDRefs.objects.filter(transitionexp=exptrans.id)
            for source in sources:
                yield '[%s] ' % source.referenceid.id

            yield '</small>\n'
            



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

        yield '%s' % GetStringValue(state.specie.name)
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


    spids = set( transs.values_list('specie_id',flat=True) )

    if (len(spids)>0): 
            
        spidsname = []
        species = Species.objects.filter(pk__in=spids) #,ncomp__gt=1)
        i=0
        bars=[]
        for specie in species:
            spidsname.append(specie.name)
            subtranss = transs.filter(specie=specie)
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


    spids = set( states.values_list('specie_id',flat=True) )
    spidsname = []
    species = Species.objects.filter(pk__in=spids) #,ncomp__gt=1)
    i=0
    plots=[]
    for specie in species:
        spidsname.append(specie.name)
        substates = states.filter(specie=specie)

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


def specieslist():
    speciess = Species.objects.filter(archiveflag=0)
    for specie in speciess:
        yield "<name>%s</name> \n" % specie.name
        yield "  <inchikey>%s</inchikey> \n" % specie.inchikey
        yield "  <stoichi>%s</stoichi> \n" % specie.molecule.stoichiometricformula
        yield "  <inchikeystem>%s<inchikeystem> \n" %  GetStringValue(specie.inchikey)[0:14]

        for nm in GetStringValue(specie.molecule.trivialname).split(","):
            yield "     <trivialname>%s<trivialname> \n" % nm
#        yield "  <trivialname>%s<trivialname> " %  GetStringValue(specie.molecule.trivialname)[0:14]
        
        yield "\n"


