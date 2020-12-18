#
# rewrite of update_functions.py
#

from datetime import datetime
import time
from node.models import *
import vamdclib.query     as vl_query
import vamdclib.results   as vl_results
import vamdclib.request   as vl_request
import vamdclib.nodes     as vl_registry
import vamdclib.specmodel as vl_specmodel
# Do not use vamdclib.inchi as it seems to be buggy
from node.InchiInfo import InchiInfo
import traceback
import sys
from pprint import pprint
from itertools import chain

def fill_species_names():
    """Add species names in index table."""
    not_deprecated_names = \
        VamdcNodeSpecies.objects.filter(deprecated=0).values_list(
                "database_species_name_id", flat=True)

    species1 = VamdcSpeciesNames.objects.all().values_list(
                "name", 'species_id', 'id')

    for value in species1:
        if value[0] != "" and value[2] in not_deprecated_names:
            VamdcSpeciesSearch.objects.get_or_create(
                value=value[0], species=VamdcSpecies.objects.get(pk=value[1]))


def fill_species_formula():
    """Add species formula in index table."""
    not_deprecated_formula = \
        VamdcNodeSpecies.objects.filter(deprecated=0).values_list(
            "database_species_formula_id", flat=True)

    species2 = VamdcSpeciesStructFormulae.objects.all().values_list(
            "formula", 'species_id', 'id')

    for value in species2:
        if value[0] != "" and value[2] in not_deprecated_formula:
            VamdcSpeciesSearch.objects.get_or_create(
                value=value[0], species=VamdcSpecies.objects.get(pk=value[1]))


def fill_species_stoichiometry():
    """Add species stoichiometry in index table."""
    species3 = VamdcSpecies.objects.all().values_list(
            "stoichiometric_formula", 'id')

    for value in species3:
        if value[0] != "":
            VamdcSpeciesSearch.objects.get_or_create(
                value=value[0], species=VamdcSpecies.objects.get(pk=value[1]))


def fill_search_table():
    """Create and populate the index table to provide search functions."""
    VamdcSpeciesSearch.objects.all().delete()
    fill_species_names()
    fill_species_formula()
    fill_species_stoichiometry()


def check_deprecated_species():
    """Verify if a species has been updated."""
    species = VamdcNodeSpecies.objects.all()   
   
    for sp in species:      
      last_species_seen_timestamp = time.mktime(datetime.strptime(sp.last_seen_dateTime.strftime("%y-%m-%d"), "%y-%m-%d").timetuple())
      last_node_update_timestamp =  time.mktime(datetime.strptime(sp.member_database.last_update_date.strftime("%y-%m-%d"), "%y-%m-%d").timetuple())
      
      # deprecated after one week
      if last_node_update_timestamp > last_species_seen_timestamp + 1209600 :
        sp.deprecated = True
        sp.save()
  

def update_nodes():
    """
    #Search for nodes in the registry, update or create records in the database
    """

    print("### query the registry for active nodes")
    nodelist = vl_registry.Nodelist()
    print(nodelist)
    nowtime = datetime.now()

    # Add new nodes or update the existing ones
    for node in nodelist:
        print("### node infos : ")
        print(node.name)
        print(node.identifier)
        print(node.url)
        print(node.maintainer)
        print(node.referenceUrl)
        db_node, created = VamdcNodes.objects.get_or_create(ivo_identifier=node.identifier)
        if created:
            print("Adding new node %s %s nn %s nu %s em"%(node.identifier, node.name, node.url, node.maintainer))            
            db_node.short_name = node.name
            db_node.contact_email = node.maintainer
            db_node.reference_url = node.referenceUrl
            db_node.status = RecordStatus.NEW
            db_node.update_status = UpdateStatus.NEW
            db_node.last_update_date = nowtime
            set_node_topics(db_node, node)
        else:
          # update only if update_status asks to do it
          if db_node.update_status == 1 :
            print("Updating the node information for %s" % db_node.short_name)
            db_node.contact_email = node.maintainer
            db_node.last_update_date = nowtime
            #~ set_node_topics(db_node, node)
        db_node.save()

def set_node_topics(db_node, node):
    """
    #add a list of topics to a keyword according to its returnables
    """
    print("adding keyword topics")
    node_topics = []
    topics = VamdcTopics.objects.all()

    for topic in topics:
      for returnable in node.returnables:
        # some nodes descriptions are lower case in dev registry
        if topic.prefix.lower() in returnable.lower() and topic.name not in node_topics:
          nodetopic = VamdcNodesTopics()
          nodetopic.node = db_node
          nodetopic.topic = topic
          nodetopic.save()
          node_topics.append(topic.name)

def query_active_nodes():
    """
    #Update species for nodes that are marked active
    """
    vl_nl = vl_registry.Nodelist()
    updated_nodes = VamdcNodes.objects.filter(update_status=UpdateStatus.ACTIVE)
    print("%s node(s) have update_status = active and will be updated."%len(updated_nodes))   
    for db_node in updated_nodes:
        try:
            vl_node = vl_nl.getnode(db_node.ivo_identifier)
            print("Process species for node %s" % vl_node.name)
            load_species(vl_node)
        except Exception as e:
            print("failed to process the node %s (%s)" % (db_node.short_name, db_node.ivo_identifier))
            print(e)
            traceback.print_exc(file=sys.stdout)


def load_species(vl_node):
    """
    Load and update node species
    """
    # ---------------------------------------------------------------------------------
    # Retrieve the data from the node using SELECT SPECIES
    vl_atoms, vl_molecules = get_species(vl_node)
    db_node = VamdcNodes.objects.get(ivo_identifier=vl_node.identifier)

    # Update or insert the atoms in the database
    for atomid in vl_atoms:
        vl_atom = vl_atoms[atomid]
        try:
            verify_atom(vl_atom)
            db_atom = update_atom(vl_atom, db_node)
            species_name = update_atom_names(db_atom, vl_atom)
            update_species_in_node(db_node, db_atom, vl_atom, species_name)
        except Exception as e:
            print("Failed to load atom:", e)
            pprint(vl_atom)
            traceback.print_exc(file=sys.stdout)

    # Update or insert the molecules
    for moleculeid in vl_molecules:
        vl_molecule = vl_molecules[moleculeid]
        try:
            vl_molecule = verify_molecule(vl_molecule)
            db_molecule = update_molecule(vl_molecule, db_node)
            species_name = update_molecule_names(db_molecule, vl_molecule)
            species_formula = update_structural_formula(db_molecule, vl_molecule.OrdinaryStructuralFormula)
            update_species_in_node(db_node, db_molecule, vl_molecule, species_name, species_formula)
        except  Exception as e:
            print("Failed to load molecule:", e)
            pprint(vl_molecule)
            traceback.print_exc(file=sys.stdout)


def update_structural_formula(db_molecule, formula, checkonly = False):
    """
    """
    # Check if it is already in the species-database
    structformulae = VamdcSpeciesStructFormulae.objects.filter(species = db_molecule.id, formula = formula)
    markup_type = VamdcMarkupTypes.objects.get(name="TEXT")

    # Insert formula into the species-database if not found
    if len(structformulae) == 0:
        # determine the search-priority. There is no automatic way
        # to determine it, so new entries
        # will be added with the highest priority
        search_priorities = VamdcSpeciesStructFormulae.objects.filter(species = db_molecule.id).values_list("search_priority", flat = True)
        if len(search_priorities) > 0:
            search_priority = max(search_priorities)
        else:
            search_priority = 1

        if checkonly is False:
            specie = VamdcSpecies.objects.get(id=db_molecule.id)
            structformula = VamdcSpeciesStructFormulae()
            structformula.species = specie
            structformula.formula = formula
            # Currently only pure text markup-type can be retrieved via XSAMS
            structformula.markup_type = markup_type
            structformula.search_priority = search_priority
            structformula.created = datetime.now()
            structformula.save()
            return structformula
        else:
            print("%s %s" % (id, formula))
    else:
      if len(structformulae) == 1:
        return structformulae.first()
      else:
        #raise Exception("error")
        print("### ERROR : struct formula size : %s" % len(structformulae))
        sys.exit()




def verify_atom(vl_atom):
    speciesid = None
    try :
      speciesid = vl_atom.VAMDCSpeciesID
    # VAMDCSpeciesID field does not exist 
    except Exception as e :
      print(e)
      
    if speciesid is None or len(speciesid) < 27:
        raise ValueError("Bad speciesid for atom '%s'" % vl_atom.ChemicalElementSymbol)
    symbol = vl_atom.ChemicalElementSymbol
    try:
        atom = VamdcDictAtoms.objects.filter(symbol=symbol)
        if len(atom) == 0:
            raise ValueError("Atom '%s' not found in the atoms dictionary." % symbol)
    except:
        raise ValueError("Atom '%s' not found in the atoms dictionary." % symbol)
    return vl_atom


def update_atom(vl_atom, db_node):
    """
    Insert or update the atom record, coming for the node

    Args:
        vl_atom (vamdclib atom):
    """
    speciesid = vl_atom.VAMDCSpeciesID
    species_type = VamdcSpeciesTypes.objects.get(name="ATOM")
    try:
      ioncharge = int(vl_atom.IonCharge)
    except:
      print("ion charge %s is not an integer" % vl_atom.IonCharge)

    try:
        massnumber = vl_atom.MassNumber
    except:
        try:
            db_dict_atom = VamdcDictAtoms.objects.get(symbol=vl_atom.ChemicalElementSymbol, most_abundant=1)
            massnumber = db_dict_atom.mass_number
        except:
            massnumber = 0

    db_atom, created = VamdcSpecies.objects.get_or_create(
        defaults={
            'origin_member_database': db_node,
            'mass_number': massnumber,
            'charge': ioncharge,
            'species_type': species_type,
        },
        id=speciesid,
    )

    if created:
        db_atom.inchi = vl_atom.InChI
        db_atom.inchikey = vl_atom.InChIKey
        db_atom.stoichiometric_formula = vl_atom.ChemicalElementSymbol
        db_atom.species_type = species_type
        db_atom.status = RecordStatus.NEW
        db_atom.update_status = UpdateStatus.NEW
        print ("adding atom %s %s" % (db_atom.stoichiometric_formula, db_atom.charge))
        db_atom.save()
    else:
        print ("found atom %s %d" % (db_atom.stoichiometric_formula, db_atom.charge))

    return db_atom

def update_atom_names(db_atom, vl_atom):
    symbol = db_atom.stoichiometric_formula
    mass = int(db_atom.mass_number)
    markup_type = VamdcMarkupTypes.objects.get(name="TEXT")
    try:
      atomname = VamdcDictAtoms.objects.filter(symbol=symbol, mass_number=mass)[0]

      if db_atom.charge > 0:
          stringname = "%s positive ion %d" % (atomname.name, db_atom.charge)
      elif db_atom.charge < 0:
          stringname = "%s negative ion %d" % (atomname.name, db_atom.charge)
      else:
          stringname=atomname.name

      db_speciesname,created = VamdcSpeciesNames.objects.get_or_create(
          defaults={
              'search_priority': -1,
              'created': datetime.now(),
              'markup_type': markup_type,
          },
          species=db_atom,
          name=stringname,
      )
      return db_speciesname
    except:
        traceback.print_exc(file=sys.stdout)
        print ("Unable to find atom $s (m %s) in the dictionary" % (symbol, mass))
    return None



def verify_molecule(vl_molecule):
    speciesid = None
    try :
      speciesid = vl_molecule.VAMDCSpeciesID
    # VAMDCSpeciesID field does not exist 
    except Exception as e :
      print(e)

    print("### INCHIKEY")
    print(vl_molecule.InChIKey)
    
    print("### SPECIES ID 1")
    print(speciesid)

    if speciesid is None or len(speciesid) < 27:
        speciesid = vl_molecule.InChIKey
        print("### SPECIES ID 2")
        print(speciesid)
        #TODO: handle multiple inchikeys/conformers here?
        if speciesid is None or len(speciesid) < 27:
            raise ValueError("Bad speciesid for molecule '%s'" % vl_molecule.StoichiometricFormula)

    vl_molecule.VAMDCSpeciesID = speciesid

    try:
        inchiinfo = InchiInfo(vl_molecule.InChI)
    except:
        print ("Unable to load the inchi information for molecule '%s'" % vl_molecule.StoichiometricFormula )
        traceback.print_exc(file=sys.stdout)
        inchiinfo = None

    try:
        mass = int(round(float(vl_molecule.MolecularWeight)))
    except:
        if (inchiinfo is None):
            mass = 0
            print ("Warning: no molecular mass information\
                    and no inchi present, setting weight to zero")
        else:
            mass = int(inchiinfo.weight)


    if (inchiinfo is not None and int(inchiinfo.weight) != mass):
        print (
        "Warning: molecular weight from Inchi (%d) does not match the XSAMS weight %d" % (int(inchiinfo.weight), mass))
    vl_molecule.MolecularWeight = mass

    try:
        charge = int(vl_molecule.IonCharge)
    except:
        if (inchiinfo is None):
            charge = 0
            print ("Warning: no charge information and no inchi present,\
                   setting charge to zero")
        else:
            charge = inchiinfo.totalCharge
    if (inchiinfo is not None and inchiinfo.totalCharge != charge):
        print ("Warning: charge from Inchi (%d) does not match XSAMS charge %d" % (inchiinfo.totalCharge, charge))
    vl_molecule.IonCharge=charge

    return vl_molecule


def update_molecule(vl_molecule, db_node):
    speciesid = vl_molecule.VAMDCSpeciesID
    molecularweight = vl_molecule.MolecularWeight
    species_type = VamdcSpeciesTypes.objects.get(name="molecule")
    try:
      charge = int(vl_molecule.IonCharge)
    except:
      print("charge value %s is not an integer" % vl_molecule.IonCharge)

    db_molecule, created = VamdcSpecies.objects.get_or_create(
        defaults={
            'origin_member_database': db_node,
            'mass_number': molecularweight,
            'charge': charge,
            'species_type': species_type
        },
        id=speciesid,
    )

    if created:
        db_molecule.inchi = vl_molecule.InChI
        db_molecule.inchikey = vl_molecule.InChIKey
        db_molecule.stoichiometric_formula = vl_molecule.StoichiometricFormula
        db_molecule.species_type = species_type
        db_molecule.status = RecordStatus.NEW
        db_molecule.update_status = UpdateStatus.NEW
        print ("adding molecule %s %s" % (db_molecule.stoichiometric_formula, db_molecule.charge))
        db_molecule.save()
    else:
        print ("found molecule %s %d" % (db_molecule.stoichiometric_formula, db_molecule.charge))

    assert isinstance(db_molecule, VamdcSpecies)
    return db_molecule


def update_molecule_names(db_molecule, vl_molecule):
    db_speciesname = None
    markup_type = VamdcMarkupTypes.objects.get(name="TEXT")
    try:
      if (vl_molecule.ChemicalName is not None):
          #Do not try to loop over names here, since there are coma-containing names.
          db_speciesname,created = VamdcSpeciesNames.objects.get_or_create(
              defaults={
                  'search_priority': -1,
                  'created': datetime.now(),
                  'markup_type': markup_type,
              },
              species=db_molecule,
              name=vl_molecule.ChemicalName,
          )
    except AttributeError as e:
      print(e)

    return db_speciesname


def update_species_in_node(db_node, db_species, vl_species, species_name, species_formula=None):
    """
    Insert or update the information on the species contained in the node
    """
    db_nodeSpecies, created = VamdcNodeSpecies.objects.get_or_create(
        species=db_species,
        member_database=db_node,
        database_species_id=vl_species.SpeciesID,
        database_species_name=species_name,
        database_species_formula=species_formula)

    if not created:
        db_nodeSpecies.last_seen_dateTime = datetime.now()
        db_nodeSpecies.save()

    if created:
        db_nodeSpecies.deprecated = False
        db_nodeSpecies.save()


def get_species(vl_node):
    """
    Retrieves a dictionary with species available at the specified node

    """

    # ------------------------------------------------------------------
    # Query data from the node via SELECT SPECIES
    query = vl_query.Query()
    request = vl_request.Request()

    query_string = "SELECT Species"
    # query_string = "SELECT SPECIES WHERE ((InchiKey!='UGFAIRIUMAVXCW'))"
    request.setnode(vl_node)
    request.setquery(query_string)

    result = request.dorequest()

    try:
        result.populate_model()
    except Exception as e:
        print(" Error: Could not process data ")
    # ------------------------------------------------------------------
    # Return Molecules and Atoms
    try:
        molecules = result.data['Molecules']
    except:
        molecules = []
    try:
        atoms = result.data['Atoms']
    except:
        atoms = []

    return atoms, molecules
