import time
from datetime import datetime
from  node.models import VamdcSpecies, VamdcNodeSpecies, VamdcSpeciesNames, VamdcSpeciesSearch, VamdcSpeciesStructFormulae
import node.import_functions as update
from node.InchiInfo import InchiInfo

def check_deprecated_species():
    """ Verify if a species has been updated. A species is marked as deprecated after 45 days (3888000 seconds)
    
    """
    species = VamdcNodeSpecies.objects.all()   
   
    for sp in species:      
      last_species_seen_timestamp = time.mktime(datetime.strptime(sp.last_seen_dateTime.strftime("%y-%m-%d"), "%y-%m-%d").timetuple())
      last_node_update_timestamp =  time.mktime(datetime.strptime(sp.member_database.last_update_date.strftime("%y-%m-%d"), "%y-%m-%d").timetuple())
      
      # deprecated after 45 days
      if last_node_update_timestamp > last_species_seen_timestamp + 3888000 :
        sp.deprecated = True
        sp.save()


def fill_species_names():
    """ Add species names in vamdc_merged_fields_vals table."""
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
    """Add species formula in vamdc_merged_fields_vals table."""
    not_deprecated_formula = \
        VamdcNodeSpecies.objects.filter(deprecated=0).values_list(
            "database_species_formula_id", flat=True)

    species2 = VamdcSpeciesStructFormulae.objects.all().values_list(
            "formula", 'species_id', 'id')

    for value in species2:
        if value[0] != "" and value[2] in not_deprecated_formula:
            VamdcSpeciesSearch.objects.get_or_create(
                value=value[0], species=VamdcSpecies.objects.get(pk=value[1]))


def fill_species_inchi_inchikey_stoichiometry():
    """Add species inchi, inchikey and stoichiometry in vamdc_merged_fields_vals table."""
    not_deprecated_species=VamdcNodeSpecies.objects.filter(deprecated=0)
    for value in not_deprecated_species:
        VamdcSpeciesSearch.objects.get_or_create(
                value=value.species.inchikey, species=value.species)
        VamdcSpeciesSearch.objects.get_or_create(
                value=value.species.inchi, species=value.species)
        VamdcSpeciesSearch.objects.get_or_create(
                value=value.species.stoichiometric_formula, species=value.species)

def fill_search_table():
    """ Update the vamdc_merged_fields_vals table to provide search functions.
        Existing content is removed an imported again
    
    """
    VamdcSpeciesSearch.objects.all().delete()
    fill_species_names()
    fill_species_formula()
    fill_species_inchi_inchikey_stoichiometry()


def fix_species_values():
    """ Update content of vamdc_species tables :  mass value for species where it is == 0 
        and inchi if it is not properly written

    """
    db_molecule = VamdcSpecies.objects.filter(mass_number=0)
    for mol in db_molecule:
        inchiinfo = InchiInfo(update.get_clean_inchi(mol.inchi))
        mol.inchi = update.get_clean_inchi(mol.inchi)
        mol.mass_number = update.get_species_mass(0, inchiinfo)
        mol.save(update_fields=["mass_number", "inchi"])