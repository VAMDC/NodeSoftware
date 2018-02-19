from datetime import datetime

from models import *

import vamdclib.query as q
import vamdclib.results
import vamdclib.request as r
import vamdclib.nodes
import vamdclib.specmodel
from vamdclib.inchi import *

from vamdclib.settings import *

import traceback
import sys

from vamdclib.nodes import Nodelist


def update_nodes():
    print "query the registry for active nodes"
    nl=Nodelist()
    ivoaids=[]
    nowtime=datetime.now()

    #for node in nl:
    #  ivoaids.append(node.identifier)

    #Update the nodes last seen
    #VamdcMemberDatabases.objects.filter(ivo_identifier__in = ivoaids).update(last_update_date=nowtime)

    #Add new nodes or update the existing ones
    for node in nl:
      db_node, created = VamdcMemberDatabases.objects.get_or_create(ivo_identifier = node.identifier)
      if created:
        print "new node "+node.identifier+" nn"+node.name+" nu"+node.url+" em"+node.maintainer+"\n"
        db_node.short_name = node.name
        db_node.contact_email = node.maintainer
        db_node.status=0
        db_node.last_update_date = nowtime
      else:
	print "Updating data for node "+db_node.short_name
        db_node.contact_email = node.maintainer
        db_node.last_update_date = nowtime
      db_node.save()


def query_active_nodes():
    vl_nl=Nodelist()
    print('### test ')
    for db_node in VamdcMemberDatabases.objects.filter( status = RecordStatus.ACTIVE ):
       try:
         vl_node=vl_nl.getnode(db_node.ivo_identifier)
         print "### Process species for node "+vl_node.name
         process_species(vl_node)
       except:
	 print "failed to process the node %s (%s)"%(db_node.short_name,db_node.ivo_identifier)






def get_db_node(ivoaid):
    """
    Returns the id of the node which is stored int the species-database
    """
    return VamdcMemberDatabases.objects.get(ivo_identifier = ivoaid)

def get_species(vl_node):
    """
    Retrieves a dictionary with species available at the specified node

    nodename: short_name of the node, which is stored in the database
    """

    #------------------------------------------------------------------
    # Query data from the node via SELECT SPECIES
    query = q.Query()
    request = r.Request()

    query_string = "SELECT SPECIES"
    #query_string = "SELECT SPECIES WHERE ((InchiKey!='UGFAIRIUMAVXCW'))"
    request.setnode(vl_node)
    request.setquery(query_string)

    result = request.dorequest()

    try:
        result.populate_model()
    except:
        print " Error: Could not process data "
    #------------------------------------------------------------------
    # Return Molecules and Atoms

    Molecules = result.data['Molecules']
    Atoms = result.data['Atoms']

    return Atoms, Molecules


def get_vamdcspeciesid(inchikey):
    """
    Returns a list of vamdcspecies-id from the database for the
    given inchikey. In most cases a list with only one id is returned.
    """
    ids = VamdcSpecies.objects.filter(inchikey = inchikey).values_list('id', flat = True)
    return ids

def process_species(vl_node, checkonly = False):
    print('### process species ')
    #---------------------------------------------------------------------------------
    # Retrieve the data from the database node
    atoms, molecules = get_species(vl_node)
    node_db_id=get_db_node(vl_node.identifier).id

    #----------------------------------------------------------------------------------
    # Loop through all the species and insert the data if the species is not yet in the
    # VamdcSpeciesDB

    for atomid in atoms:
        # Get atom - object
        atom = atoms[atomid]
        atom.IonCharge = int(atom.IonCharge)
        try:
            if atom.IonCharge == 0:
                stoichiometricformula = "%s" % (atom.ChemicalElementSymbol)
            elif atom.IonCharge == 1:
                stoichiometricformula = "%s+" % (atom.ChemicalElementSymbol)
            elif atom.IonCharge == -1:
                stoichiometricformula = "%s-" % (atom.ChemicalElementSymbol)
            elif atom.IonCharge > 1:
                stoichiometricformula = "%s+%d" % (atom.ChemicalElementSymbol, atom.IonCharge)
            elif atom.IonCharge < 1:
                stoichiometricformula = "%s%d" % (atom.ChemicalElementSymbol, atom.IonCharge)
            atom.StoichiometricFormula = stoichiometricformula
        except:
            pass

        #------------------------------------------------------------
        # Insert specie into database (will be inserted only if not already present)
        id =insert_atom(atom, member_db_id = node_db_id, checkonly = checkonly)
        # skip the rest of the loop if a specie could not be identified
        #
        # PROBLEM: Currently there is no treatment in the rest of this procedure
        #          if more than one species is identified by the same inchikey.
        if id is None:
            continue

        #------------------------------------------------------------
        # Insert names for the specie
        #insert_species_name(id, name, checkonly = checkonly)

        #-----------------------------------------------------------
        # Insert structural formula
        if atom.IonCharge == 0:
            formula = "%s" % (atom.ChemicalElementSymbol)
        elif atom.IonCharge == 1:
            formula = "%s+" % (atom.ChemicalElementSymbol)
        elif atom.IonCharge == -1:
            formula = "%s-" % (atom.ChemicalElementSymbol)
        elif atom.IonCharge > 1:
            formula = "%s+%d" % (atom.ChemicalElementSymbol, atom.IonCharge)
        elif atom.IonCharge < 1:
            formula = "%s%d" % (atom.ChemicalElementSymbol, atom.IonCharge)


        insert_structural_formula(id, formula, checkonly = checkonly)

        #-----------------------------------------------------------
        # Insert nodes species-id
        insert_member_db_speciesid(id, node_db_id, atom.SpeciesID, checkonly = checkonly)



    for moleculeid in molecules:
        # Get molecule - object
        molecule = molecules[moleculeid]

        #------------------------------------------------------------
        # Insert specie into database (will be inserted only if not already present)
        id =insert_molecule(molecule, member_db_id = node_db_id, checkonly = checkonly)
        print('### molecule inserted : %s'%id)
        # skip the rest of the loop if a specie could not be identified
        #
        # PROBLEM: Currently there is no treatment in the rest of this procedure
        #          if more than one species is identified by the same inchikey.
        if id is None:
            continue

        #------------------------------------------------------------
        # Insert names for the specie
        # The element ChemicalName cannot be repeated in current XSAMS versions. A list
        # of names has to be separated by ', ' therefore.
        try:
            names = molecule.ChemicalName.split(', ')
        except AttributeError:
            names = []
        for name in names:
            insert_species_name(id, name, checkonly = checkonly)

        #-----------------------------------------------------------
        # Insert structural formula
        print('### structural formula ')
        insert_structural_formula(id, molecule.OrdinaryStructuralFormula, checkonly = checkonly)

        #-----------------------------------------------------------
        # Insert nodes species-id
        insert_member_db_speciesid(id, node_db_id, molecule.SpeciesID, checkonly = checkonly)


def insert_molecule(molecule, member_db_id = 0, checkonly = False):
    """
    Insert Molecule into VAMDC-Species-DB

    checkonly: Boolean (if True, data will be printed and NOT inserted into database)
    """

    # If InChIKey is not determined insert has to be skiped
    try:
        inchikey = molecule.InChIKey
    except:
        print "InChIKey is not available: Skip insert"
        return None

    # VamdcSpecies - Table
    vamdcspeciesid = molecule.InChIKey

    # check if molecule is already in database
    ids = get_vamdcspeciesid(molecule.InChIKey)

    # If exactly one species is identified by the InChIKey than
    # just return the VamdcSpeciesID. As there is currently no
    # treatment for the case if more than one species is returned
    # the return value for this case is None.
    if len(ids) == 1:
        return ids[0]
    elif len(ids) > 1:
        return None

    try:
        inchi = molecule.InChI
    except:
        inchi = ''

    try:
        inchi_info = InChI(inchi)
    except Exception, e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print "Could not parse InChI: %s" % inchi
        print e
        traceback.print_exc(file=sys.stdout)
        traceback.print_exception(exc_type, exc_value, exc_traceback,
                              limit=2, file=sys.stdout)
        return None

    charge = inchi_info.charge #get_charge(inchi)
    stoichiometricformula = inchi_info.stoichiometric_formula
    molecular_weight = inchi_info.massnumber

    # compare if stoichiometric formula matches the one in the query-result
    try:
        if stoichiometricformula != molecule.StoichiometricFormula:
            print "MISMATCH Formula: %s does not match %s" % (stoichiometricformula, molecule.StoichiometricFormula)
    except AttributeError:
        print "DETERMINED Formula: %s" % molecule.StoichiometricFormula

    try:
        if molecular_weight != int(float(molecule.MolecularWeight)):
           print "MISMATCH mass: %d does not match %d" % (molecular_weight, int(float(molecule.MolecularWeight)))
    except AttributeError:
        print "DETERMINED mass: %d" % molecular_weight

    if checkonly == False:
        specie = VamdcSpecies()

        member_database = VamdcMemberDatabases.objects.get(id = member_db_id)

        specie.id = inchikey
        specie.inchi = inchi
        specie.inchikey = inchikey
        specie.inchikey_duplicate_counter = 1
        specie.stoichiometric_formula = stoichiometricformula
        specie.species_type = SpeciesType.MOLECULE
        specie.created = datetime.now()
        specie.member_database = member_database
        specie.mass_number = molecular_weight
        specie.charge = charge

        #    cml = m.cml
        #    mol = models.CharField(max_length=765, blank=True)
        #    image = models.CharField(max_length=765, blank=True)
        #    smiles = models.TextField(blank=True)

        specie.save()
    else:
        print "%-20s %-40s %-10s %-4s %4d %4d" % (inchikey,
                                                  inchi,
                                                  stoichiometricformula,
                                                  charge,
                                                  member_db_id,
                                                  molecular_weight)

    return vamdcspeciesid


def insert_atom(atom, member_db_id = 0, checkonly = False):
    """
    Insert Atom into VAMDC-Species-DB

    checkonly: Boolean (if True, data will be printed and NOT inserted into database)
    """

    # VamdcSpecies - Table
    try:
        vamdcspeciesid = atom.InChIKey
    except:
        print "InChIKey is not available: Skip insert"
        return None

    # check if atom is already in database
    ids = get_vamdcspeciesid(atom.InChIKey)

    # Insert atom into database if not found
    # If exactly one species is identified by the InChIKey than
    # just return the VamdcSpeciesID. As there is currently no
    # treatment for the case if more than one species is returned
    # the return value for this case is None.
    if len(ids) == 1:
        return ids[0]
    elif len(ids) > 1:
        return None

    print "Insert Atom: %s" % atom.InChIKey
    print ids

    try:
        inchi = atom.InChI
    except:
        inchi = ''

    try:
      inchi_info = InChI(inchi)
      charge = inchi_info.charge #get_charge(inchi)
      stoichiometricformula = inchi_info.stoichiometric_formula
      massnumber = inchi_info.massnumber

      # compare if stoichiometric formula matches the one in the query-result
      try:
        if stoichiometricformula != atom.StoichiometricFormula:
           print "MISMATCH Formula: %s does not match %s" % (stoichiometricformula, atom.StoichiometricFormula)
      except AttributeError:
        print "DETERMINED Formula: %s" % stoichiometricformula

      try:
        if massnumber != int(atom.MassNumber):
            print "MISMATCH mass: %d does not match %d" % (massnumber, int(atom.MassNumber))
      except AttributeError:
        atom.MassNumber = massnumber
        print "DETERMINED mass: %d" % massnumber
    except:
      print "failed parsing inchi %s" %inchi



    if checkonly == False:
        member_database = VamdcMemberDatabases.objects.get(id = member_db_id)
        specie = VamdcSpecies()

        specie.id = atom.InChIKey
        #if atom.InChI[:6] == 'InChI=':
        #    specie.inchi = atom.InChI
        #else:
        #    specie.inchi = 'InChI='+atom.InChI
        specie.inchikey = atom.InChIKey
        #specie.inchikey_duplicate_counter = 1
        specie.stoichiometric_formula = atom.StoichiometricFormula
        specie.species_type = SpeciesType.ATOM
        specie.created = datetime.now()
        specie.member_database = member_database
        specie.mass_number = atom.MassNumber
        specie.charge = 0 #TODO: how do we handle ions in speciesdb?

        #    charge = m.Charge
        #    cml = m.cml
        #    mol = models.CharField(max_length=765, blank=True)
        #    image = models.CharField(max_length=765, blank=True)
        #    smiles = models.TextField(blank=True)

        specie.save()
    else:
        print "%20s %20s %10s %4d %4d" % (atom.InChIKey,
                                          atom.InChI,
                                          stoichiometricformula,
                                          member_db_id,
                                          massnumber)

    return vamdcspeciesid


def insert_structural_formula(id, formula, checkonly = False):
    """
    """
    # Check if it is already in the species-database
    structformulae = VamdcSpeciesStructFormulae.objects.filter(species = id, formula = formula)

    # Insert formula into the species-database if not found
    if len(structformulae) == 0:

        # determine the search-priority. There is no automatic way to determine it, so new entries
        # will be added with the highest priority
        search_priorities = VamdcSpeciesStructFormulae.objects.filter(species = id).values_list("search_priority", flat = True)
        if len(search_priorities)>0:
            search_priority = max(search_priorities)
        else:
            search_priority = 1

        if checkonly == False:
            specie = VamdcSpecies.objects.get(id = id)
            structformula = VamdcSpeciesStructFormulae()
            structformula.species = specie
            structformula.formula = formula
            # Currently only pure text markup-type can be retrieved via XSAMS
            structformula.markup_type = MarkupTypes.TEXT
            structformula.search_priority = search_priority
            structformula.created = datetime.now()
            structformula.save()
        else:
            print "%s %s" % (id, formula)



def insert_species_name(id, name, checkonly = False):
    """
    """
    # Check if it is already in the species-database
    names = VamdcSpeciesNames.objects.filter(species = id, name = name)


    # Insert name into the species-database if not found
    if len(names) == 0:

        # determine the search-priority. There is no automatic way to determine it, so new entries
        # will be added with the highest priority
        search_priorities = VamdcSpeciesNames.objects.filter(species = id).values_list("search_priority", flat = True)
        if len(search_priorities)>0:
            search_priority = max(search_priorities)+1
        else:
            search_priority = 1

        if checkonly == False:
            specie = VamdcSpecies.objects.get(id = id)
            speciesname = VamdcSpeciesNames()
            speciesname.species = specie
            speciesname.name = name
            # Currently only pure text markup-type can be retrieved via XSAMS
            speciesname.markup_type = MarkupTypes.TEXT
            speciesname.search_priority = search_priority
            speciesname.created = datetime.now()

            speciesname.save()
        else:
            print "%s %s" % (id, name)

def insert_member_db_speciesid(id, member_db_id, speciesid, checkonly = False):
    """
    Inserts the Species-ID available at a specific database node into
    the species-database.

    id = VamdcSpeciesID (Inchikey)
    member_db_id = id of the database node
    speciesid = id of the specie in the database node
    checkonly = Boolean (False if the data is inserted in the database, otherwise it is only printed)
    """
    # Check if it is already in the species-database
    dbidentifier = VamdcMemberDatabaseIdentifiers.objects.filter(species = id, member_database = member_db_id, database_species_id = speciesid)
    print "%20s %2d %20s" % (id, member_db_id, speciesid)
   # Insert database-species-id into the species-database if not found
    if len(dbidentifier) == 0:

        if checkonly == False:
            specie = VamdcSpecies.objects.get(id = id)
            member_database = VamdcMemberDatabases.objects.get(id = member_db_id)

            dbidentifier = VamdcMemberDatabaseIdentifiers()
            dbidentifier.species = specie
            dbidentifier.member_database = member_database
            dbidentifier.database_species_id = speciesid
            print
            dbidentifier.save()
        else:
            print "%20s %2d %20s" % (id, member_db_id, speciesid)
