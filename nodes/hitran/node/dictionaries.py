# -*- coding: utf-8 -*-

from vamdctap.caselessdict import CaselessDict

RETURNABLES=CaselessDict({\
'SourceID':'Refs.sourceid',
'SourceAuthorName':'Refs.author',
'SourceTitle':'Refs.title',
# NB my Refs model has pages, not page_begin and page_end:
'SourcePageBegin':'Refs.pages',		
'SourceVolume':'Refs.volume',
'SourceYear':'Refs.year',
'SourceName':'Refs.journal',    # closest we can get to the journal name

'RadTransComments':'',
'RadTransFinalStateRef':'RadTran.finalstateref',
'RadTransInitialStateRef':'RadTran.initialstateref',
'RadTransWavenumberExperimentalValue':'RadTran.nu',
'RadTransWavenumberExperimentalSourceRef':'RadTran.nu_ref',
'RadTransWavenumberExperimentalAccuracy':'RadTran.nu_err',
'RadTransProbabilityTransitionProbabilityAValue':'RadTran.a',
'RadTransProbabilityTransitionProbabilityASourceRef':'RadTran.a_ref',
'RadTransProbabilityTransitionProbabilityAAccuracy':'RadTran.a_err',
'RadTransProbabilityProbability:MultipoleValue':'RadTran.multipole',

'MolecularSpeciesChemicalName':'Molecule.chemical_names',
'MolecularSpeciesOrdinaryStructuralFormula':'Molecule.molec_name',
'MolecularSpeciesOrdinaryStoichiometricFormula': \
        'Molecule.stoichiometric_formula',

'MolecularStateStateID':'MolState.stateid',
'MolecularStateEnergyValue':'MolState.energy',
'MolecularStateEnergyUnit':'cm-1',
'MolecularStateEnergyOrigin':'Zero-point energy',
'MolecularStateCharacTotalStatisticalWeight':'MolState.g',

'MolQnStateID': 'MolQN.stateid',
'MolQnCase': 'MolQN.case',      # e.g. 'dcs', 'ltcs', ...
'MolQnLabel': 'MolQN.label',    # e.g. 'J', 'asSym', ...
'MolQnValue': 'MolQN.value'
})

RESTRICTABLES = CaselessDict({\
'Inchikey':'inchikey',
'RadTransWavenumberExperimentalValue':'nu',
'RadTransProbabilityTransitionProbabilityAValue':'a',
})

# work out which molecules are present in the database ...
loaded_molecules = Trans.objects.values('molecid').distinct()
# ... and get their names and html-names from the molecules table:
molecules = Molecules.objects.filter(molecid__in=loaded_molecules).values(
        'molecid','molec_name','molec_name_html')
# Do the same for molecules with cross sections in the HITRAN database:
xsec_molecules = Molecules.objects.filter(molecid__in=Xsec.objects.values(
        'molecid').distinct()).values('molecid','molec_name','molec_name_html')

# metadata concerning the quantum numbers in the case-by-case description,
# retrieved from the QNdesc table and used by the parseHITRANstates method:
case_desc = QNdesc.objects.values('caseid', 'case_prefix', 'name', 'col_index',
                                  'col_name')

case_prefixes = {}
case_prefixes[1] = 'dcs'
case_prefixes[5] = 'nltcs'

def index(request):
    c=RequestContext(request,{})
    return render_to_response('index.html', c)


#counter=0
def poll(request):
	#counter+=1
	#return_text = '<p>%d -*-</p>' % counter
	return_text = '<p>Woop!</p>'
	#if counter>10:
	#	return_text='END OF JOB'
	return HttpResponse(return_text)

def search_lbl(request):
	if request.POST:
		# translate the query string into a dictionary:
		# e.g. 'numin=0.&numax=100.&...' -> {'numin': 0., 'numax': 100., ...}
		q = QueryDict(request.POST['post_data'])
		numin = q.get('numin')
		if numin: numin=float(numin)
		numax = q.get('numax')
		if numax: numax=float(numax)
		Smin = q.get('Smin')
		if Smin: Smin=float(Smin)

		# The form returns molecule=<molecID> for any checked
        # <molec_name> boxes:
		selected_molecids = q.getlist('molecule')
		selected_molecules = Molecules.objects.filter(
            molecid__in=selected_molecids).values(
                    'molec_name','molec_name_html')

		# here's where the real work is done:
		start = time.time()
		req = make_request(numin, numax, Smin, selected_molecids,
                           output_params = None,
                           output_formats = 'par',
                           compression = None)
		HITRAN.read_db_from_mysql(req,'christian','whatever')
		finish = time.time()
		
		return HttpResponse('Hello Sir!')

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

	selected_output_fields = ['nu','S']
	available_output_fields = ['A','g_air','g_self','n_air',
        'delta_air','QN-upper','QN-lower']
	return render_to_response('search_lbl.html',
		{'molec_cb_html': molec_cb_html,
		'available_output_fields': available_output_fields,
		'selected_output_fields': selected_output_fields})

def search_xsec(request):
	return render_to_response('search_xsec.html',
        {'xsec_molecules': xsec_molecules})

def custom_sync(request):
    """
    Customized view for HITRAN TAP query, using HITRAN-specific
    XSAMS generator routines.

    """
    tap = TapQuery(request.REQUEST)
    if not tap.isvalid:
        LOG('Request is not valid TAP')
        return HttpResponse('Failed to parse TAP request')

    sql = tap.parsedSQL
    q = sqlparse.where2q(sql.where, RESTRICTABLES)
    try:
        q = eval(q)
    except Exception, e:
        LOG('Exception in setupResults():')
        LOG(e)
        return HttpResponse('Failed to parse SQL request.')

    # get the transitions
    transitions = Trans.objects.filter(q)

    # get the states
    stateIDs = set([])
    for transition in transitions:
        stateIDs = stateIDs.union([transition.initialstateref,
                                   transition.finalstateref])
    states = AllStates.objects.filter(pk__in=stateIDs)

    # get the molecules
    molecIDs = set([])
    for transition in transitions:
        molecIDs = molecIDs.union([transition.molecid])
    molecules = Molecules.objects.filter(pk__in=molecIDs)

    # get the sources
    sourceIDs = set(['B_HITRAN2008'])
    for transition in transitions:
        s = set([transition.nu_ref, transition.a_ref])
        sourceIDs = sourceIDs.union(s)
    sources = Refs.objects.filter(pk__in=sourceIDs)

    ##response = ['<h2>HITRAN tap query results</h2>']
    ##for transition in transitions:
        ##response.append('<p>%12.6f</p>' % transition.nu)
    ##return HttpResponse('\n'.join(response))

    generator = xsams_generator(transitions, states, molecules, sources)
    response = HttpResponse(generator, mimetype='application/xml')
    return response

###############################################################################
# legacy code, in which the TAP interface is handled generically
# using Thomas Marquart's routines in DjNode:

def getHITRANstates(transs):
    stateIDs = set([])
    for trans in transs:
        stateIDs = stateIDs.union([trans.initialstateref,
                                   trans.finalstateref])

    return AllStates.objects.filter(pk__in=stateIDs)

def getHITRANmolecules(transs):
    molecIDs = set([])
    for trans in transs:
        molecIDs = molecIDs.union([trans.molecid])
    return Molecules.objects.filter(pk__in=molecIDs)

def getHITRANsources(transs):
    sourceIDs = set([])
    for trans in transs:
        s = set([trans.nu_ref, trans.a_ref])
        sourceIDs = sourceIDs.union(s)
    return Refs.objects.filter(pk__in=sourceIDs)

def parseHITRANstates(states):
    qns = []
    sids=set([])
    for state in states:
        s=set([state.stateid])
        sids=sids.union(s)

    for qn in AllQns.objects.filter(stateid__in=sids):
        label, value = qn.qn.split('=')
        qns.append(MolQN(qn.stateid, case_prefixes[qn.caseid], label, value))

    LOG('%d state quantum numbers obtained' % len(qns))
    #sys.exit(0)
    return qns

def setupResults(sql):
    q = sqlparse.where2q(sql.where,RESTRICTABLES)
    try:
        q=eval(q)
    except Exception,e:
        LOG('Exception in setupResults():')
        LOG(e)
        return {}

    transs = Trans.objects.filter(q) 
    sources = getHITRANsources(transs)
    states = getHITRANstates(transs)
    # extract the state quantum numbers in a form that generators.py can use:
    qns = parseHITRANstates(states)
    molecules = getHITRANmolecules(transs)
    LOG('%s transitions retrieved from HITRAN database' % transs.count())
    LOG('%s states retrieved from HITRAN database' % states.count())

   # return the dictionary as described above
    return {'RadTrans': transs,
            'Sources': sources,
            'MoleStates': states,
            'MoleQNs': qns,
            'Molecules': molecules}
