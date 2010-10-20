# -*- coding: utf-8 -*-

from django.http import HttpResponse, QueryDict
from django.shortcuts import render_to_response,get_object_or_404
from django.template import RequestContext
from django.utils import simplejson
import time
from django.db.models import Q

# import your models 
from DjHITRAN.HITRAN.models import *

import DjNode.tapservice.sqlparse as sqlparse
from tap import TapQuery
from xsams_generator import *

#import os
#import sys
#PROJECT_ROOT = os.path.dirname(__file__)
#sys.path.insert(0, os.path.join(PROJECT_ROOT, "DjNode"))

### IMPORTANT NOTE This file must implement a function called 
### setupResults() which takes the parsed SQL from the query parser. 
### setupResults() must pass the restrictions on to one or several of 
### your models (depending on the database strcture) and also fetch the 
### corresponding items from other models that are needed in the return 
### data. setupResults() must return a DICTIONARY that has as keys some 
### of the following: Sources AtomStates MoleStates CollTrans RadTrans 
### Methods; with the corresponding QuerySets as the values for these 
### keys. This dictionary will be handed into the generator an allow it 
### to fill the XML schema.
###
### Below is an example, inspired by VALD that has a data model like 
### this:
### One for the Sources/References
### One for the Species
### One for the States (points to Species once, and to several 
###   references)
### One for Transitions (points twice to States (upper, lower) and to 
###   several Sources)
###
### In this layout, all restrictions in the query can be passed to
### the Transitions model (using the pointers between models to
### restrict eg. Transition.species.ionization) which facilitates
### things.
###
### Now we can code two helper functions that get the corresponding
### Sources and States to a selection of Transitions:

# a straight forward example of getting the unique list of
# states that correspond to a given list of transitions by
# use of the inverse foreign key.

import sys
def LOG(s):
    print >> sys.stderr, s

# In order to map the global keywords that come in the query
# to the place in the data model where the corresponding data sits, we 
# use two dictionaries, called RESTRICTABLES and RETURNABLES.

RETURNABLES={\
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

'MolecularSpeciesChemicalName':'MolState.chemical_names',
'MolecularSpeciesOrdinaryStructuralFormula':'MolState.molec_name',
'MolecularSpeciesOrdinaryStoichiometricFormula': \
        'MolState.stoichiometric_formula',

'MolecularStateStateID':'MolState.stateid',
'MolecularStateEnergyValue':'MolState.energy',
'MolecularStateEnergyUnit':'cm-1',
'MolecularStateEnergyOrigin':'Zero-point energy',
'MolecularStateCharacTotalStatisticalWeight':'MolState.g',

}

RESTRICTABLES = {\
'SpeciesID':'molecid',
'RadTransWavenumberExperimentalValue':'nu',
'RadTransProbabilityTransitionProbabilityAValue':'a',
}

# work out which molecules are present in the database ...
loaded_molecules = Trans.objects.values('molecid').distinct()
# ... and get their names and html-names from the molecules table:
molecules = Molecules.objects.filter(molecid__in=loaded_molecules).values(
        'molecid','molec_name','molec_name_html')
# Do the same for molecules with cross sections in the HITRAN database:
xsec_molecules = Molecules.objects.filter(molecid__in=Xsec.objects.values(
        'molecid').distinct()).values('molecid','molec_name','molec_name_html')

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

def sync(request):
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

#def getHITRANstates(transs):
    #statepps = AllStates.objects.filter(isstatepp_trans__in = transs)
    #stateps = AllStates.objects.filter(isstatep_trans__in = transs)
    #states = statepps | stateps
    #return states.distinct()

#    stateIDs = set([])
#    for trans in transs:
#        stateIDs = stateIDs.union([trans.initialstateref,
#                                   trans.finalstateref])

#    molecIDs = []
#    for trans in transs:
#        if trans.molecid not in molecIDs:
#            molecIDs.append(trans.molecid)

#    return AllStates.objects.filter(pk__in=stateIDs) & \
#                Molecules.objects.filter(pk__in=molecIDs)

#def getHITRANsources(transs):
#    sourceIDs = set([])
#    for trans in transs:
#        s = set([trans.nu_ref, trans.a_ref])
#        sourceIDs = sourceIDs.union(s)
#    return Refs.objects.filter(pk__in=sourceIDs)
    
#def setupResults(sql):
#    q=where2q(sql.where,RESTRICTABLES)
#    try:
#        q=eval(q)
#    except Exception,e:
#        LOG('Exception in setupResults():')
#        LOG(e)
#        return {}

#    transs = Trans.objects.filter(q) 
#    sources = getHITRANsources(transs)
#    states = getHITRANstates(transs)
#    LOG('%s transitions retrieved from HITRAN database' % transs.count())
#    LOG('%s states retrieved from HITRAN database' % states.count())

    # return the dictionary as described above
#    return {'RadTrans': transs,
#            'Sources': sources,
#            'MoleStates': states}
