# -*- coding: utf-8 -*
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
from vamdctap.sqlparse import *
from vamdctap.sqlparse import sql2Q

from math import sqrt, trunc

import dictionaries
import models # this imports models.py from the same directory as this file

from django.db.models import Q
import re

from inchivalidation import inchikey2chemicalformula

def LOG(s):
    #josis logfunction
    logfilejosi = open('/var/log/vamdc_josi.log','a')
    s=str(s)
    logfilejosi.write(s + '\n')

#generic empty class
class GenericClass:
    pass

#create class for datasets
class DataSet:
    """
    this class provides a method to make the Tabulated sub-objects out of two tuples containing the x and y values
    """

    def __init__(self,sourceref,xs,ys,productiondate):
        #put reference to source first, so we always know what it is
        self.SourceRef = sourceref
        self.TabData = []

        tabdata = GenericClass()
        tabdata.Xunits = 'eV'
        tabdata.ProductionDate = productiondate
        tabdata.X = GenericClass()
        tabdata.Y = GenericClass()
        tabdata.X.AccuracyType = 'estimated'
        tabdata.Y.AccuracyType = 'statistical'
        tabdata.X.Relative = 'false'
        tabdata.Y.Relative = 'false'
        tabdata.X.ErrorValue = float('0.1')
        tabdata.X.SourceRef = sourceref
        #i know this is bad crap crazy, but the standards want it like this
        #uncomment the float as we do it in the energyscan-loop already when reading the data
        #tabdata.X.DataList = map(float,xs)
        #tabdata.Y.DataList = map(float,ys)
        tabdata.X.DataList = map(str,xs)
        tabdata.Y.DataList = map(str,ys)
        
        tabdata.Xlength = len(xs)
        tabdata.Ylength = len(ys)

        #create errors
        tabdata.Y.ErrorList = []
        yerrorlist = map(sqrt,ys)
        for yerror in yerrorlist:
            tabdata.Y.ErrorList.append("%.2f" % round(yerror,2))

        self.TabData.append(tabdata)

# create electron statically, as it is always involved and always the same
#particles.append()
class Particle:
    def __init__(self,type):
        if type == 'electron':
            self.charge = -1
            self.name = 'electron'
            self.speciesid = 'electron'
            self.comment = 'low energy electrons'

#------------------------------------------------------------
# Main function 
#------------------------------------------------------------

def setupResults(sql, limit=1000):
    """
    This function is always called by the software.
    """
    # log the incoming query
    LOG(sql)

    #x_internal is the list for the iteration over one search result, x the overall list (which is deduplicated in the end)
    
    molecules = []
    molecules_internal = []
    atoms = []
    atoms_internal = []
    sources = []
    sources_internal = []
    particles = []
    electron_particle = Particle('electron')

    #use the function sql2Q provided by vamdctap to translate from query to Q-object
    q = sql2Q(sql)

    #create queryset for energyscans according to query
    energyscans = models.Energyscan.objects.filter(q)

    # count the number of matches
    nenergyscans=energyscans.count()

    #in case somebody is searching for a InchiKey and it didn't bring up any results:
    #convert the inchikey to an inchi, extract the sum formula and try again
    if nenergyscans == 0:
        if re.search('InchiKey', str(sql)) is not None:
            match = re.search('[A-Z]{14}-[A-Z]{10}-[A-Z]', str(sql))
            inchikey = str(sql)[match.start():match.end()]
            chemical_formula = inchikey2chemicalformula(inchikey)

            #now we extracted the stochiometric / chemical formula from the inchi. 
            #let's see if there is something in the DB
            if chemical_formula is not None:
                energyscans = models.Energyscan.objects.filter(Q(species__chemical_formula__exact=chemical_formula)|Q(origin_species__chemical_formula__exact=chemical_formula))
                nenergyscans=energyscans.count()

    #append electron if there are results:
    if nenergyscans != 0:
        particles.append(electron_particle)

    #loop over energyscans that came back

    for energyscan in energyscans:
        #our reactants are always molecules. here we check if the product is a molecule.
        if energyscan.species.molecule:
            molecules_internal = models.Species.objects.filter(Q(id__exact=energyscan.species.id)|Q(id__exact=energyscan.origin_species.id))
        else:
            atoms_internal = models.Species.objects.filter(Q(id__exact=energyscan.species.id))
            molecules_internal = models.Species.objects.filter(Q(id__exact=energyscan.origin_species.id))

        energyscan.Products = models.Species.objects.filter(id__exact=energyscan.species.id)
        energyscan.Reactants = models.Species.objects.filter(id__exact=energyscan.origin_species.id)

        #this part is a bit tricky: we make a new species-object which we give the ID 'electron'. otherwise it is empty
        #then we use list on the queryset energyscan.Reactants to force it to be executed.
        #afterwards, we append the newly created electron instance of the class species

        #keep in mind, that we actually defined the particle electron further up in the Particle() class. it was instanciated in the beginning of this function under the object electron_particle
        
        electron = models.Species('electron','','','','')
        energyscan.Reactants = list(energyscan.Reactants.all())
        energyscan.Reactants.append(electron)

        #make products negative
        for product in energyscan.Products:
            for molecule in molecules_internal:
                if product.id == molecule.id:
                    molecule.ioncharge = -1
                else:
                    molecule.ioncharge = 0                    
            for atom in atoms_internal:
                if product.id == atom.id:
                    atom.ioncharge = -1
                else:
                    atom.ioncharge = 0

        sources_internal = models.Source.objects.filter(id__exact=energyscan.source.id)
        for source in sources_internal:
            authorlist=[]
            for author in source.authors.all():
                authorlist.append(u'%s, %s'%(author.lastname,author.firstname))

            source.author = authorlist

        #insert the standard-comment in addition to a possibly existing user-specific comment
        standardcomment = 'X-Values are measured with an energy resolution of %s eV. Therefore every shown peak is the original peak shape convoluted with our resolution. Energy scans are calibrated. Therefore we estimate an error of 0.1 eV' % energyscan.energyresolution 

        if energyscan.comment != '':
            usercomment = energyscan.comment
            energyscan.comment = 'Comment of the Producer: ' + usercomment + ' Additional Comment: ' + standardcomment
        else:
            energyscan.comment = standardcomment 

        #prepare the origin data
        ES_list = energyscan.energyscan_data.split()
        k = 0
        x = []
        y = []
        for datapoint in ES_list:
            datapoint = datapoint.replace(',','.')
            #even -> x-value
            if k%2 == 0:
                x.append(float(datapoint))
            #odd -> y-value
            else: 
                y.append(float(datapoint))
            k = k + 1

        if len(x) != len(y):
            LOG('WARNING - number of x and y values is not equal')

        #create datasets
        energyscan.DataSets = []
        dataset = DataSet(energyscan.source.id,x,y,energyscan.productiondate)
        dataset.description = 'crossSection'
        dataset.accuracytype = 'systematic'
        energyscan.DataSets.append(dataset)

        #here we combine the list for molecules, atoms and sources from this particular energyscan with the query-wide list and remove all duplicates
        #see http://stackoverflow.com/questions/1319338/combining-two-lists-and-removing-duplicates-without-removing-duplicates-in-orig
        molecules = molecules + list(set(molecules_internal) - set(molecules))
        atoms = atoms + list(set(atoms_internal) - set(atoms))
        sources = sources + list(set(sources_internal) - set(sources))

    #count species and sources in order to return it to the headerinfo

    nsources = len(sources)
    nmolecules = len(molecules)
    natoms = len(atoms)
    nspecies = natoms + nmolecules

    # Create the header with some useful info. The key names here are
    # standardized and shouldn't be changed.
    headerinfo={\
            'COUNT-SOURCES':nsources,
            'COUNT-SPECIES':nspecies,
            'COUNT-ATOMS':natoms,
            'COUNT-MOLECULES':nmolecules,
            'COUNT-COLLISIONS':nenergyscans,
            'COUNT-STATES':0,
            'COUNT-RADIATIVE':0,
            'COUNT-NONRADIATIVE':0,
            }

    # Return the data if it is not empty... The keynames are standardized. 
    if nenergyscans > 0:
        return {'CollTrans':energyscans,
                'Sources':sources,
                'Atoms':atoms,
                'Molecules':molecules,
                'Particles':particles,
                'HeaderInfo':headerinfo,
               }
    else:
        return {}
