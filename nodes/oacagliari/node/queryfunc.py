# -*- coding: utf-8 -*-
#
# This module (which must have the name queryfunc.py) is responsible
# for converting incoming queries to a database query understood by
# this particular node's database schema.
# 
# This module must contain a function setupResults, taking a sql object
# as its only argument. 
#

# library imports 

import sys
from itertools import chain
from django.conf import settings
from vamdctap.sqlparse import where2q, splitWhere, mergeQwithLogic, restriction2Q


import dictionaries

import models # this imports models.py from the same directory as this file
from SOAPpy.wstools.WSDLTools import Element
from django.db.models import Q


def LOG(s):
    "Simple logger function"
    if settings.DEBUG: print >> sys.stderr, s

#------------------------------------------------------------
# Helper functions (called from setupResults)
#------------------------------------------------------------
def MoleculeNormalModeHarmonicFrequency_MHz2cm(op, foo):
    """
    Making the conversion from MHz to cm-1.
    """

    opp = op

    try:
        foop = float(foo[0].replace("'", "").replace('"', ''))
    except (ValueError, TypeError):
        print 'failed to convert %s to float' % foo
        return None
    except (IndexError):
        print 'no argument to MoleculeNormalModeHarmonicFrequency restrictable'
        return None
    if foop != 0.:
        # MHz -> cm-1
        foop =  foop / 29979.2458
    q = ['MoleculeNormalModeHarmonicFrequency', opp, str(foop)]
    return q

#------------------------------------------------------------
# Main function 
#------------------------------------------------------------


        
def builRef(id_ref):
    b = models.Bibliography.objects.get(pk = id_ref)
    return b.bibtextoref()


def setupResults(sql, limit=1000):
    """
    This function is always called by the software.
    """
    # log the incoming query
    LOG(sql)
    result_sources = [] #Sources related to results
    methods = [] #Methods related to results
    nmMethod = None
    # convert the incoming sql to a correct django query syntax object 
    # based on the RESTRICTABLES dictionary in dictionaries.py
    # (where2q is a helper function to do this for us).
    q = where2q(sql.where, dictionaries.RESTRICTABLES)
    try: 
        q = eval(q) # test queryset syntax validity
    except Exception,e:
        return {}
    # ... we parse the query into its restrictables and logic:
    if not sql.where:
        return {}
    logic, rs, count = splitWhere(sql.where)
    #Convert MoleculeNormalModeHarmonicFrequency
    # from MHz to cm-1:
    for i in rs:
        r, op, foo = rs[i][0], rs[i][1], rs[i][2:]
        if r == 'MoleculeNormalModeHarmonicFrequency':
            rs[i] = MoleculeNormalModeHarmonicFrequency_MHz2cm(op, foo)
    # now rebuild the query as a dictionary of QTypes ...
    qdict = {}
    for i, r in rs.items():
        q = restriction2Q(r)
        qdict[i] = q
    # ... and merge them to a single query object
    q = mergeQwithLogic(qdict, logic)
    # We build a queryset of database matches on the Transision model
    # since through this model (in our example) we are be able to
    # reach all other models. Note that a queryset is actually not yet
    # hitting the database, making it very efficient.
    molecularspecies = models.MolecularSpecies.objects.filter(q).distinct()

    # count the number of matches, make a simple trunkation if there are
    # too many (record the coverage in the returned header) 
    nmolecularspecies=molecularspecies.count()
    if limit < nmolecularspecies :
        nmolecularspecies = molecularspecies[:limit]
        percentage='%.1f' % (float(limit) / nmolecularspecies * 100)
    else: 
        percentage=None
    
    nspecies = molecularspecies.count()
    nstates = 0
    
    for molecular_specie in molecularspecies:
        molecular_specie.States = molecular_specie.electronicstates_set.all()
        min_energy = 0
        min_energy = min
        normalmodelist = []
        NormalModeSourceRef = []
        MoleculeStructureSourceRef = []
        for state in molecular_specie.States:
            #search minimum total energy
            state.StateEnergySourceRef = []
            state.energymethod = state.task.pk
            if not (state.energymethod in [m.id for m in methods]):
                new_method = models.Method(state.energymethod, state.task.returnmethoddescriptionandbib(), result_sources)
                result_sources += new_method.Sources
                methods.append(new_method)

            for ref in state.bibliographies.all():
                if ref.bibtex:
                    if not (ref in result_sources):
                        result_sources.append(ref)
                    state.StateEnergySourceRef.append(ref.bib_id)
            if min([min_energy, state.total_energy]) == state.total_energy:
                #we need to list all molecule structure
                MoleculeStructureMethod = state.energymethod
                MoleculeStructureSourceRef = state.StateEnergySourceRef                
                MoleculeStructure = state.geom.returncmlstructure(MoleculeStructureSourceRef)
            vibration_analyses_armonic = state.vibrationalanalysesarmonic_set.all()
            elementlist = state.geom.returnelementslist()
            
            if len(vibration_analyses_armonic) > 0:
                for vref in vibration_analyses_armonic[0].bibliographies.all():
                    if vref.bibtex:
                        if not (vref in result_sources):
                            result_sources.append(vref)
                        NormalModeSourceRef.append(vref.bib_id)
                nmMethod = vibration_analyses_armonic[0].task.pk
                if not (nmMethod in [m.id for m in methods]):
                    new_method = models.Method(nmMethod, vibration_analyses_armonic[0].task.returnmethoddescriptionandbib(), result_sources)
                    result_sources += new_method.Sources
                    methods.append(new_method)

                for tab in vibration_analyses_armonic[0].tabulatedvibrations_set.all():
                    normalmode = models.NormalMode(tab.pk, tab.frequency, tab.ir_intensity, tab.sym_type, tab.eigenvectors, state.state_id, elementlist, nmMethod, NormalModeSourceRef)
                    normalmodelist.append(normalmode)

        molecular_specie.molecularchemicalspecies = models.MolecularChemicalSpecies(MoleculeStructure, MoleculeStructureMethod, MoleculeStructureSourceRef, None, nmMethod, NormalModeSourceRef)
        if normalmodelist:
            molecular_specie.NormalModes = normalmodelist
        nstates += molecular_specie.States.count()
        molecular_specie.comments = str(molecular_specie.comments) 

    # Through the transition-matches, use our helper functions to extract 
    # all the relevant database data for our query. 

    # Create the header with some useful info. The key names here are
    # standardized and shouldn't be changed.
    nsources = len(result_sources)
    nmolecules = len(molecularspecies)
    

    if molecularspecies:
        size_estimate='%.2f'%(nmolecules*0.0014 + 0.01)
    else: size_estimate='0.00'

    headerinfo={\
            'TRUNCATED':percentage,
            'COUNT-STATES':nstates,
            'COUNT-MOLECULES': nmolecules,
            'APPROX-SIZE':size_estimate,
            }
            
    # Return the data. The keynames are standardized. 
    return {"Molecules" : molecularspecies,
            "Methods" : methods,
            'Sources':result_sources,
            'HeaderInfo':headerinfo,
           }

