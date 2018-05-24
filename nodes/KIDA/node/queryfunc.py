# -*- coding: utf-8 -*-
#
# This module (which must have the name queryfunc.py) is responsible
# for converting incoming queries to a database query understood by
# this particular node's database schema.
# 

# library imports 

import sys
from django.db.models import Q
from django.conf import settings
from vamdctap.sqlparse import where2q, sql2Q


import dictionaries
from models import *

import logging
log = logging.getLogger('vamdc.node.queryfu')

import re

from xml.sax.saxutils import escape, unescape

from pprint import pprint


if hasattr(settings,'TRANSLIM'):
    TRANSLIM = settings.TRANSLIM
else: 
    TRANSLIM = 1000

if hasattr(settings,'LAST_MODIFIED'):
    LAST_MODIFIED = settings.LAST_MODIFIED
else: 
    LAST_MODIFIED = None


class EmptyClass:
    """Empty class to add attributes dynamically to"""


html_escape_table = {
    '"': "&quot;",
    "'": "&apos;"
}

def html_escape(text):
    return escape(str(text), html_escape_table)

def html_unescape(text):
    return unescape(text, html_unescape_table)


def cleanhtml(raw_html): # fonction pour supprimer les code HTML d'un string
    if raw_html is None or len(raw_html) == 0:
        return raw_html
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext



def constraintsPresent(sql):
    return len(sql.where) > 0 
    
def setupMethods(): 
    # KIDA methods : 
    # - Calculations
    # - Estimation
    # - Measurements
    # - Reviews and Evaluations
    methods = []

    method = EmptyClass()
    method.id = 1
    method.category = 'theory'
    method.description = 'Calculations'
    methods.append(method)
    
    method = EmptyClass()
    method.id = 2
    method.category = 'evaluated'
    method.description = 'Estimation'
    methods.append(method)
    
    
    method = EmptyClass()
    method.id = 3
    method.category = 'experiment'
    method.description = 'Measurements'
    methods.append(method)
    
    method = EmptyClass()
    method.id = 4
    method.category = 'compilation'
    method.description = 'Reviews and Evaluations'
    methods.append(method)
    
    return methods
    

    
    
def setupFunctions(): #definition des formules possibles.

    functions = []
    formulas = Formula.objects.all().filter()
    
    for form in formulas:
        function = EmptyClass()
        function.id = form.id
        function.Name = form.name
        function.expression = form.math
        function.computer_language = 'math'
       
        functionYParameter = EmptyClass()
        functionYParameter.name = 'k'
        units = None
        
        if form.id == 1 or form.id == 2:
            units = '1/s'
        if form.id == 3 or form.id == 4 or form.id == 5:
            units = 'cm3/s'
        # functionYParameter.units = cleanhtml(form.units)
        functionYParameter.units = units
        functionYParameter.description = 'Rate coefficient vs temperature'
        function.Y = functionYParameter
        
        function.Arguments = []

        function.Parameters = []
            
        if form.id == 1:
            functionArguments = []
            functionArgument = EmptyClass()

            functionArgument.name = 'zeta'
            functionArgument.units = '1/s'
            functionArgument.description = 'H2 cosmic-ray ionization rate'
            functionArguments.append(functionArgument)
            function.Arguments = functionArguments
            
            
            functionParameters = []
            functionParameter = EmptyClass()
            functionParameter.name = 'alpha'
            functionParameter.units = 'unitless'
            functionParameters.append(functionParameter)
            function.Parameters = functionParameters
        
        if form.id == 2:

            functionArguments = []
            functionArgument = EmptyClass()

            functionArgument.name = 'Av'
            functionArgument.units = 'unitless'
            functionArgument.description = 'Visual extinction'
            functionArguments.append(functionArgument)
            function.Arguments = functionArguments
            
            
            functionParameters = []
            functionParameter = EmptyClass()
            functionParameter.name = 'alpha'
            functionParameter.units = '1/s'
            functionParameters.append(functionParameter) 
            functionParameter = EmptyClass()
            functionParameter.name = 'gamma'
            functionParameter.units = 'unitless'
            functionParameters.append(functionParameter) 
            function.Parameters = functionParameters
        if form.id == 3:
            functionArguments = []
            functionArgument = EmptyClass()

            functionArgument.name = 'T'
            functionArgument.units = 'K'
            functionArgument.description = 'Temperature'
            functionArguments.append(functionArgument)
            function.Arguments = functionArguments

            functionParameters = []
            functionParameter = EmptyClass()
            functionParameter.name = 'alpha'
            functionParameter.units = 'cm3/s'
            functionParameter.description = 'alpha multiplier'
            functionParameters.append(functionParameter)
            functionParameter = EmptyClass()
            functionParameter.name = 'beta'
            functionParameter.units = 'unitless'
            functionParameter.description = 'beta power'
            functionParameters.append(functionParameter)
            functionParameter = EmptyClass()
            functionParameter.name = 'gamma'
            functionParameter.units = 'K'
            functionParameter.description = 'gamma exponent'
            functionParameters.append(functionParameter)
            function.Parameters = functionParameters
        if form.id == 4 or form.id == 5: 
            functionArguments = []
            functionArgument = EmptyClass()

            functionArgument.name = 'T'
            functionArgument.units = 'K'
            functionArgument.description = 'Temperature'
            functionArguments.append(functionArgument)
            function.Arguments = functionArguments

            functionParameters = []
            functionParameter = EmptyClass()
            functionParameter.name = 'alpha'
            functionParameter.units = 'unitless'
            functionParameter.description = 'branching ratio'
            functionParameters.append(functionParameter)
            functionParameter = EmptyClass()
            functionParameter.name = 'beta'
            functionParameter.units = 'cm3/s'
            functionParameter.description = 'Langevin rate'
            functionParameters.append(functionParameter)
            functionParameter = EmptyClass()
            functionParameter.name = 'gamma'
            functionParameter.units = 'unitless'
            functionParameter.description = 'gamma parameter'
            functionParameters.append(functionParameter)
            function.Parameters = functionParameters
            
        if form.id == 6:
            continue
        if form.id == 7:
            continue
        
            
        functions.append(function)
    return functions



def union(a, b):
    return list(set(a) | set(b))


def intersect(a, b):
    if len(a) == 0:
        return list(set(b))
    return list(set(a) & set(b))


def splitSpecies(tabSpecies):
    atoms = []
    molecules = []
    particles = []
    
    
    for s in tabSpecies:
        tabSe = SpeciesHasElement.objects.all().filter(species=s)
        nbAtom = 0
        for se in tabSe:
            nbAtom = nbAtom + se.occurrence

        if nbAtom == 1:
            if s.common_name == 'CR' or s.common_name == 'CRP' or s.common_name == 'e-' or s.common_name == 'Photon':
                particles.append(s)
            else:
                element = se.element
                element.Charge = s.charge
                element.Inchi = s.inchi
                element.InchiKey = s.inchi_key
                element.Name = element.symbol
                element.SpeciesID = s.id
                
                atoms.append(element)

        else:
            molecules.append(s)
    
    
    return atoms, molecules, particles


    

    
def setupResults(sql):
    # log the incoming query
    log.debug(sql)
    


    # convert the incoming sql to a correct django query syntax object
    # (sql2Q is a helper function to do this for us).
    q = sql2Q(sql)
    
    print (sql)
    # print (q)
    
    if constraintsPresent(sql) == False:
        # SELECT SPECIES special case
        # return all species ( only with inchikey ?)
        species = Species.objects.all().filter(inchi_key__isnull=False,application="Astro")
        customKida = ['CR', 'CRP', 'Photon', 'e-']
        kidaParticles = Species.objects.all().filter(common_name__in=customKida)
        species = union (species, kidaParticles)
        atoms, molecules, particles = splitSpecies(species)
        natoms = len(atoms)
        nmolecules = len(molecules)
        nparticles = len(particles)
        headerinfo={\
            'COUNT-ATOMS':natoms,
            'COUNT-MOLECULES':nmolecules,
            'COUNT-SPECIES':natoms+nmolecules+nparticles,
            'COUNT-COLLISIONS':0
            }

    
        return {'Atoms':atoms, 
            'Molecules':molecules,
            'Particles':particles,
            'HeaderInfo':headerinfo
           }
        
    else:
        return parseComplexQuery(q)
    
        
    
def parseComplexQuery(q):
    
    # print (vars(q))
    # print (q.connector)
    # print (q.children)

    searchChannels = []
    reactantValues = {}
    productValues = {}
    
    for child in q.children:
        tabValue = []
        tabKey = []
        tabPrefix = []
        connector = q.connector
        
        
        if not isinstance(child, Q):
            print ('child')
            print (child)
            key = child[0]
            value = child[1]
            keySplit = key.split('__')
            prefix = keySplit[0]
            tabKey.append(key)
            tabValue.append(value)
            tabPrefix.append(prefix)
            
        else:
            print ('une liste')
            child2 = child.children
            connector = child.connector
            
            for sChild in child.children:
                print (sChild)
                print ('\n\n')
                key = sChild[0]
                value = sChild[1]
                keySplit = key.split('__')
                prefix = keySplit[0]
                tabKey.append(key)
                tabValue.append(value)
                tabPrefix.append(prefix)

            
        for index, key in enumerate(tabKey):
            print (tabKey[index])
            print (tabValue[index])
            print (tabPrefix[index])
            prefix = tabPrefix[index]
            value = tabValue[index]
            key = tabKey[index]
        
        
            if prefix == 'reactant':
                newKeyValue = key.replace('reactant__','')
                if not isinstance(value, list):
                    reactantValues[value] = reactantValues.get(value, 0) + 1
                    #values =  value
                #else:
                    #values =  value
                kwargs = {'%s' % (newKeyValue): value}

                #kwargs = {'%s' % (newKeyValue): values}

                reactSpecies = Species.objects.all().filter(**kwargs)



                noccurrence = 1
                if not isinstance(value, list):
                    noccurrence = reactantValues[value]
                if noccurrence > 1:
                    reactants = Reactant.objects.all().filter(species__in=reactSpecies,occurrence=noccurrence)
                else:
                    reactants = Reactant.objects.all().filter(species__in=reactSpecies)

                
                reactions = Reaction.objects.all().filter(reactant__in=reactants)
                
                channels = Channel.objects.all().filter(reaction__in=reactions)
                
                searchChannels = intersect(searchChannels, channels)



            if prefix == 'product': 
                newKeyValue = key.replace('product__','')
                if not isinstance(value, list):
                    productValues[value] = productValues.get(value, 0) + 1
                    #values =  value
                #else:
                    #values =  ",".join(value) 

                #kwargs = {'%s' % (newKeyValue): values}
                kwargs = {'%s' % (newKeyValue): value}

                prodSpecies = Species.objects.all().filter(**kwargs)
                #print ("species  " + str(len(reactSpecies)))

                noccurrence = 1
                if not isinstance(value, list):
                    noccurrence = productValues[value]
                if noccurrence > 1:
                    products = Product.objects.all().filter(species__in=prodSpecies,occurrence=noccurrence)
                else:
                    products = Product.objects.all().filter(species__in=prodSpecies)

                channels = Channel.objects.all().filter(product__in=products)
                searchChannels = intersect(searchChannels, channels)



            if prefix == 'species': 
                newKeyValue = key.replace('species__','')

                kwargs = {'%s' % (newKeyValue): value}
                species = Species.objects.all().filter(**kwargs)
                print ('nb species = ' + str(len(species)))

                products = Product.objects.all().filter(species__in=species)

                channelsProd = Channel.objects.all().filter(product__in=products)

                #searchChannels = union(searchChannels, channels)

                reactants = Reactant.objects.all().filter(species__in=species)

                reactions = Reaction.objects.all().filter(reactant__in=reactants)

                channelsReact = Channel.objects.all().filter(reaction__in=reactions)


                channels = union(channelsProd, channelsReact)
                
                print ('nb channels = ' + str(len(channels)))


                if connector == 'AND':
                    searchChannels = intersect(searchChannels, channels)
                if connector == 'OR':
                    searchChannels = union(searchChannels, channels)
                    
                print ("apres AND/OR " + str(len(searchChannels)))

            if prefix == 'source':
                newKeyValue = key.replace('source__','')

                kwargs = {'%s' % (newKeyValue): value}
                biblio = Biblio.objects.all().filter(**kwargs)

                bimo = CvBimo.objects.all().filter(biblio__in=biblio)
                channelBimo = Channel.objects.all().filter(id__in=bimo.values_list('channel'))

                cosmic = CvCosmic.objects.all().filter(biblio__in=biblio)
                channelCosmic = Channel.objects.all().filter(id__in=cosmic.values_list('channel'))

                searchChannels = union(channelBimo, channelCosmic)

            if prefix == "method":
                allMethods = setupMethods()
                # newKeyValue = key.replace('method__','')

                # filter methods by query
                methods = filter(lambda m: m.category == value, allMethods)
                # map between VAMDC method and KIDA method
                methods = map(lambda m: m.description, methods)
                bimo = CvBimo.objects.all().filter(method__in=methods)

                channelBimo = Channel.objects.all().filter(id__in=bimo.values_list('channel'))

                cosmic = CvCosmic.objects.all().filter(method__in=methods)
                channelCosmic = Channel.objects.all().filter(id__in=cosmic.values_list('channel'))

                searchChannels = union(channelBimo, channelCosmic)

            if prefix == "function":
                allFunctions = setupFunctions()
                # newKeyValue = key.replace('formula__','')

                functions = filter(lambda f: 'FKIDA-' + str(f.id) == value, allFunctions)
                functions = map(lambda m: m.id, functions)

                bimo = CvBimo.objects.all().filter(formula__in=functions)

                channelBimo = Channel.objects.all().filter(id__in=bimo.values_list('channel'))

                cosmic = CvCosmic.objects.all().filter(formula__in=functions)
                channelCosmic = Channel.objects.all().filter(id__in=cosmic.values_list('channel'))

                searchChannels = union(channelBimo, channelCosmic)
            

    relatedSpecies = []
    atoms = []
    molecules = []
    particles = []
    biblios = []
    
    
    channels = []
    
    #tabReactant = Reactant.objects.all().filter(reaction__in=searchChannels.values_list('reaction'))
    #tabProduct = Product.objects.all().filter(channel__in=searchChannels)
    
    functions = setupFunctions()
    methods = setupMethods()

    
    # equivalent a faire un array_unique
    channels = list(set(searchChannels))
    

    if TRANSLIM < len(channels):
        print ('Number of channel > ' + str(TRANSLIM) + ' : ' + str(len(channels)))
    
   
    maxChannel = len(channels)    
    truncated = 0 
    
    nbRemoved = 0
    for index, ch in enumerate(channels[:]):
        ch.Reactants = []
        ch.Products = []

        if ch.reaction.family == "Surface":
            print ('remove only surface'+ str(ch.id))
            nbRemoved += 1
            channels.remove(ch)
            continue
        
        if ch.reaction.family == "3Body":
            print ('remove only 3body' + str(ch.id))
            nbRemoved += 1
            channels.remove(ch)
            continue
        
        if ch.isOnlyPlaneto():
            print ('remove only planeto'+ str(ch.id))
            nbRemoved += 1
            channels.remove(ch)
            continue

        if ((index-nbRemoved) > TRANSLIM):
            # channels.remove(ch)
            truncated = '%.1f'%(float(TRANSLIM)/maxChannel *100)
            break
        
        react = ch.reaction.reactant_set.all()
        for r in react:
            ch.Reactants.append(r.species)
            if r.occurrence == 2:
                ch.Reactants.append(r.species)
            if r.occurrence == 3:
                ch.Reactants.append(r.species)
                ch.Reactants.append(r.species)
            relatedSpecies.append(r.species) #on stocke les especes liées, qui doivent aussi apparaitre dans le XSAMS final
            
        prod = ch.product_set.all()
        for p in prod:
            ch.Products.append(p.species)
            if p.occurrence == 2:
                ch.Products.append(p.species)
            relatedSpecies.append(p.species) #on stocke les especes liées, qui doivent aussi apparaitre dans le XSAMS final


        ch.DataSets = []
        
        # en fait le channel est soit bimo, soit cosmic, soit termo, soit surface
        ch.Bimos = CvBimo.objects.all().filter(channel=ch)
        ch.Cosmics = CvCosmic.objects.all().filter(channel=ch)
        # ch.Termos = CvTermo.objects.all().filter(channel=ch)
        
        for bimo in ch.Bimos:
            if bimo.application == "Planeto":
                continue
            dataset = EmptyClass()
            
            
            fitDataClass = EmptyClass()

            fitDataArgument = EmptyClass()
            fitDataArguments = []

            fitDataArgument.tmin = bimo.tmin
            fitDataArgument.tmax = bimo.tmax
            fitDataArgument.description = 'Temperature'
            fitDataArgument.name = 'T'
            fitDataArgument.units = 'K'
                
            fitDataArguments.append(fitDataArgument)

            fitDataParameter = EmptyClass()
            if bimo.formula.id == 3:
                fitDataParameter.parameter = [bimo.alpha, bimo.beta, bimo.gamma]
                fitDataParameter.names = ['alpha', 'beta', 'gamma']
                fitDataParameter.units = ['cm3/s', 'unitless', 'K']
            if bimo.formula.id == 4:
                fitDataParameter.parameter = [bimo.alpha, bimo.beta, bimo.gamma]
                fitDataParameter.names = ['alpha', 'beta', 'gamma']
                fitDataParameter.units = ['unitless', 'cm3/s', 'unitless']
            if bimo.formula.id == 5:
                fitDataParameter.parameter = [bimo.alpha, bimo.beta, bimo.gamma]
                fitDataParameter.names = ['alpha', 'beta', 'gamma']
                fitDataParameter.units = ['unitless', 'cm3/s', 'unitless']

            fitDataParameters = []
            

            fitDataParameters.append(fitDataParameter)
            fitDataClass.Arguments = fitDataArguments
            fitDataClass.Parameters = fitDataParameters
            fitDataClass.functionref = bimo.formula.id
            fitDataClass.method = None
            if bimo.method == 'Calculations':
                fitDataClass.method = 1
            if bimo.method == 'Estimation':
                fitDataClass.method = 2
            if bimo.method == 'Measurements':
                fitDataClass.method = 3
            if bimo.method == 'Reviews and Evaluations':
                fitDataClass.method = 4
            
       
            fitDataClass.uncert = str(bimo.f0) + " (" + bimo.type_uncert_f+ ")" 
            fitDataClass.date = bimo.updatedat.strftime("%Y-%m-%d")
            
            Evaluations = []
            Evaluation = EmptyClass()
            Evaluation.recommended = False
            if bimo.expertize == 3:
                Evaluation.recommended = True
            Evaluation.quality = str(bimo.expertize)
            Evaluations.append(Evaluation)
            
            fitDataClass.Evaluations = Evaluations
            
            fitDataClass.biblio = None
            if bimo.biblio is not None:
                fitDataClass.biblio = bimo.biblio.id
                biblios.append(bimo.biblio)
            

            dataset.FitData = [fitDataClass]
            dataset.description = 'rateCoefficient'
        
            ch.DataSets.append(dataset)

        for cosmic in ch.Cosmics:
            if cosmic.application == "Planeto":
                continue
                
            dataset = EmptyClass()
            
            
            fitDataClass = EmptyClass()

            fitDataParameter = EmptyClass()
            if cosmic.formula.id == 1:
                fitDataArgument = EmptyClass()
                fitDataArguments = []

                fitDataArgument.description = 'H2 cosmic-ray ionization rate'
                fitDataArgument.name = 'zeta'
                fitDataArgument.units = '1/s'
                fitDataArgument.tmin = None
                fitDataArgument.tmax = None
                fitDataArguments.append(fitDataArgument)

                fitDataParameter.parameter = [cosmic.alpha]
                fitDataParameter.names = ['alpha']
                fitDataParameter.units = ['unitless']
            if cosmic.formula.id == 2:
                
                fitDataArgument = EmptyClass()
                fitDataArguments = []

                fitDataArgument.description = 'Visual Extinction'
                fitDataArgument.name = 'Av'
                fitDataArgument.units = '1/s'
                fitDataArgument.tmin = None
                fitDataArgument.tmax = None
                fitDataArguments.append(fitDataArgument)
                
                
                fitDataParameter.parameter = [cosmic.alpha, cosmic.gamma]
                fitDataParameter.names = ['alpha', 'gamma']
                fitDataParameter.units = ['1/s', 'unitless']
            
            fitDataParameters = []
            

            fitDataParameters.append(fitDataParameter)
            fitDataClass.Arguments = fitDataArguments
            fitDataClass.Parameters = fitDataParameters
            fitDataClass.functionref = cosmic.formula.id
            fitDataClass.method = None
            if cosmic.method == 'Calculations':
                fitDataClass.method = 1
            if cosmic.method == 'Estimation':
                fitDataClass.method = 2
            if cosmic.method == 'Measurements':
                fitDataClass.method = 3
            if cosmic.method == 'Reviews and Evaluations':
                fitDataClass.method = 4
            
       
            fitDataClass.uncert = str(cosmic.f0) + " (" + cosmic.type_uncert_f+ ")"
            fitDataClass.date = cosmic.updatedat.strftime("%Y-%m-%d")
            
            
            Evaluations = []
            Evaluation = EmptyClass()
            Evaluation.recommended = False
            if cosmic.expertize == 3:
                Evaluation.recommended = True
            Evaluation.quality = str(cosmic.expertize)
            Evaluations.append(Evaluation)
            
            fitDataClass.Evaluations = Evaluations
            
            fitDataClass.biblio = None
            if cosmic.biblio is not None:
                fitDataClass.biblio = cosmic.biblio.id
                biblios.append(cosmic.biblio)
            

            dataset.FitData = [fitDataClass]
            dataset.description = 'rateCoefficient'
        
            ch.DataSets.append(dataset)
    
    print ("avant truncated" + str(len(channels)))
    if truncated > 0:
        channels = channels[0:TRANSLIM]
    print ("apres truncated" + str(len(channels)))
    
    relatedSpecies = list(set(relatedSpecies))
    
    atoms, molecules, particles = splitSpecies(relatedSpecies)
    

    sources = list(set(biblios))
    for s in sources:
        pagebegin = ''
        pageend = ''
        volume = ''
        sourcename = None
        category = ''
        journal = s.get_Journal()
        book = s.get_Book()
        
        
        if journal is not None:
            volumePage = journal.page
            if volumePage is not None:
                volumePage = volumePage.split(',')
                volume = volumePage[0]
                if len(volumePage) > 1 and volumePage[1] is not None:
                    pages = volumePage[1]
                    if pages is not None:
                        pages = pages.split('-')
                        pagebegin = pages[0]
                        if len(pages) > 1 and pages[1] is not None:
                            pageend = pages[1]
                            if pageend == '':
                                pageend = pagebegin
                        else:
                            pageend = pagebegin
            
            sourcename = journal.journal
            category = 'journal'
        
        if book is not None:
            pages = book.pages
            if pages is not None:
                pages = pages.split('-')
                pagebegin = pages[0]
                if len(pages) > 1 and pages[1] is not None:
                    pageend = pages[1]
                else:
                    pageend = pagebegin
            
            sourcename = book.booktitle
            category = 'book'
        

        s.pagebegin = pagebegin.lstrip().rstrip()
        s.pageend = pageend.lstrip().rstrip()
        s.volume = volume.lstrip().rstrip()
        s.sourcename = html_escape(sourcename)
        s.category = category
        s.titreXML = ''
        if s.title is not None:
            s.titleXML = html_escape(s.title.encode("utf8"))


    nsources = len(sources)
    nparticles = len(particles)
    nmolecules = len(molecules)
    natoms = len(atoms)
    ncoll = len(channels)
    

    print ('Number of channel (after truncated) ' + str(ncoll))
    
    if ncoll+nmolecules+nsources+natoms+nparticles>0:
        size_estimate='%.2f'%(ncoll*0.0014 + 0.01)
    else: size_estimate='0.00'

    headerinfo={\
            'COUNT-ATOMS':natoms,
            'COUNT-MOLECULES':nmolecules,
            'COUNT-SPECIES':natoms+nmolecules+nparticles,
            'COUNT-COLLISIONS':ncoll,
            'APPROX-SIZE':size_estimate
            }

    if truncated > 0:
        headerinfo['TRUNCATED'] = truncated
    
    
    return {'Atoms':atoms, 
            'Molecules':molecules,
            'Particles':particles,
            'CollTrans':channels,
            'Sources':sources,
            'Functions':functions,
            'Methods':methods,
            'HeaderInfo':headerinfo
           }

   

