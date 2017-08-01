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
from django.conf import settings
from vamdctap.sqlparse import *
from vamdctap.sqlparse import sql2Q

from math import sqrt

import node.dictionaries
import node.models as models # this imports models.py from the same directory as this file

from django.db.models import Q
import re

from node.inchivalidation import inchikey2chemicalformula
import node.chemlib as chemlib

#in order to deal with the Last Modified header
import time
import datetime

#to deal with (un)escaped URLs
from xml.sax.saxutils import escape, unescape

def LOG(s):
    """ logfunction. will be removed for final version. """
    logfilejosi = open('/var/log/vamdc_josi.log','a')
    s = str(s)
    logfilejosi.write(s + '\n')

#generic empty class
class GenericClass:
    """return empty class"""
    pass

#create class for datasets
class DataSet:
    """
    this class provides a method to make the Tabulated sub-objects out of two tuples containing the x and y values
    """

    def __init__(self, xs, ys, productiondate, y_units):
        self.TabData = []

        tabdata = GenericClass()
        tabdata.Xunits = 'eV'
        tabdata.Yunits = y_units
        tabdata.ProductionDate = productiondate
        tabdata.X = GenericClass()
        tabdata.Y = GenericClass()
        tabdata.X.AccuracyType = 'estimated'
        tabdata.Y.AccuracyType = 'statistical'
        tabdata.X.Relative = 'false'
        tabdata.Y.Relative = 'false'
        tabdata.X.ErrorValue = float('0.1')
        #i know this is bad crap crazy, but the standards want it like this
        #uncomment the float as we do it in the energyscan-loop already when reading the data
        #tabdata.X.DataList = map(float,xs)
        #tabdata.Y.DataList = map(float,ys)
        tabdata.X.DataList = map(str, xs)
        tabdata.Y.DataList = map(str, ys)
        
        tabdata.Xlength = len(xs)
        tabdata.Ylength = len(ys)

        #create errors
        tabdata.Y.ErrorList = []
        #apparently we have to take the abs, since there can be negative data
        yerrorlist = map(abs, ys)
        yerrorlist = map(sqrt, yerrorlist)
        for yerror in yerrorlist:
            tabdata.Y.ErrorList.append("%.2f" % round(yerror, 2))

        self.TabData.append(tabdata)

# create electron statically, as it is always involved and always the same
#particles.append()
class Particle:
    """Provide class for particles. Only used for electrons as of now"""
    def __init__(self, type):
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

    inchiconvertedsearch = False

    #define the last modified header with an old date. we will compare all timestamps to this and take the most recent one
    lastmodifiedheader = datetime.datetime(1970, 1, 1, 1, 1)

    #use the function sql2Q provided by vamdctap to translate from query to Q-object
    q = sql2Q(sql)

    #create queryset for energyscans according to query
    energyscans = models.Energyscan.objects.filter(q)

    # count the number of matches
    nenergyscans = energyscans.count()

    #in case somebody is searching for a InchiKey and it didn't bring up any results:
    #convert the inchikey to an inchi, extract the sum formula and try again
    if nenergyscans == 0:
        if re.search('InchiKey', str(sql)) is not None:
            strsql = str(sql)
            match = re.findall('[A-Z]{14}-[A-Z]{10}-[A-Z]', strsql)

            #for each inchikey found we extract the chemical formula from the inchi
            #then we replace it in the original sql string
            for matchitem in match:
                chemical_formula = inchikey2chemicalformula(matchitem)
                if chemical_formula is not None:
                    strsql = strsql.replace(matchitem, chemical_formula)

            #if we had found one, we now replace the query
            if match is not None:
                strsql = strsql.replace('InchiKey','MoleculeStoichiometricFormula')
                #we now inject the new query to the request and call validate() to parse the SQL
                sql.request['QUERY'] = strsql
                sql.validate()

                #try again as usual
                energyscans = models.Energyscan.objects.filter(q)
                nenergyscans = energyscans.count()
                inchiconvertedsearch = True

    #append electron if there are results:
    if nenergyscans != 0:
        particles.append(electron_particle)

    #loop over energyscans that came back

    for energyscan in energyscans:
        #compare if lastmodified is newer than then newest we have already included
        if energyscan.lastmodified > lastmodifiedheader:
            lastmodifiedheader = energyscan.lastmodified

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

        electron = models.Species('electron', '', '', '', '')
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

        #calculate exact / nominal masses
        for atom in atoms_internal:
            if molecule.isotope is True:
                atom.exactmass = chemlib.chemicalformula2exactmass(atom.chemical_formula)

        for molecule in molecules_internal:
            if molecule.isotope is True:
                molecule.mass = chemlib.chemicalformula2exactmass(molecule.chemical_formula)

        #treat sources
        sources_internal = models.Source.objects.filter(id__exact=energyscan.source.id)
        for source in sources_internal:
            authorlist = []
            for author in source.authors.all():
                authorlist.append(u'%s, %s'%(author.lastname, author.firstname))

            source.author = authorlist

            #unescape and escape the URL again. this prevents us from delivering ampersands and therefore creating invalid XSAMS documents
            source.url = escape(unescape(source.url))

        #insert the standard-comment in addition to a possibly existing user-specific comment
        standardcomment = 'X-Values are measured with an energy resolution of %s eV. Therefore every shown peak is the original peak shape convoluted with our resolution. Energy scans are calibrated. Therefore we estimate an error of 0.1 eV' % energyscan.energyresolution 

        if energyscan.comment != '':
            usercomment = energyscan.comment
            energyscan.comment = 'Comment of the Producer: ' + usercomment + ' Additional Comment: ' + standardcomment
        else:
            energyscan.comment = standardcomment 

        #give warning when we converted inchikey to chemical formula for searching
        if inchiconvertedsearch is True:
            inchiwarning = 'WARNING: For this query, an InChI-Key was converted to a stoichiometric formula, because otherwise no results were obtained. '
            energyscan.comment = inchiwarning + energyscan.comment

        #prepare the origin data
        ES_list = energyscan.energyscan_data.split()
        k = 0
        x = []
        y = []
        for datapoint in ES_list:
            datapoint = datapoint.replace(',','.')
            #even -> x-value
            if k % 2 == 0:
                x.append(float(datapoint))
            #odd -> y-value
            else:
                y.append(float(datapoint))
            k = k + 1

        if len(x) != len(y):
            LOG('WARNING - number of x and y values is not equal')

        #create datasets
        energyscan.DataSets = []
        dataset = DataSet(x, y, energyscan.productiondate, energyscan.y_units)
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

    #Create the Last Modified header
    #the header must not be newer than now!
    if lastmodifiedheader > datetime.datetime.now():
        lastmodifiedheader = datetime.datetime.now()

    # Create the header with some useful info. The key names here are
    # standardized and shouldn't be changed.
    headerinfo = {\
            'COUNT-SOURCES':nsources,
            'COUNT-SPECIES':nspecies,
            'COUNT-ATOMS':natoms,
            'COUNT-MOLECULES':nmolecules,
            'COUNT-COLLISIONS':nenergyscans,
            'COUNT-STATES':0,
            'COUNT-RADIATIVE':0,
            'COUNT-NONRADIATIVE':0,
            'LAST-MODIFIED':lastmodifiedheader,
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
