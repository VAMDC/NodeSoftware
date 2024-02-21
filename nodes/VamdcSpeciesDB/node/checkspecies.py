from node.models import *
from pyvalem.formula import Formula
from re import search

def checkmass():
    allspecies = VamdcSpecies.objects.all().order_by('stoichiometric_formula', 'charge')

    print("{0: <12} # {1: <6} # {2: <7} # {3: <12} # {4: <75} # {5: <125}".format("species", "charge",  "db_mass", "pyvalem_mass", "inchi", "warning"))

    for species in allspecies:
       if search(r"i[0-9]+[+|-][0-9]+", species.inchi) is None and species.mass_number > 0:
            try : 

                species_name = '{}'.format(species.stoichiometric_formula.replace(" ", ""))
                species_charge = '{}'.format(species.charge)
                species_inchi = '{}'.format(species.inchi)
                pyvalem_mass = '{}'.format(round(Formula(species.stoichiometric_formula).mass))
                db_mass = '{}'.format(species.mass_number)

                if pyvalem_mass != db_mass:
                    alert = " !! masses are different !! Pyvalem not rounded : {0: <10}".format(Formula(species.stoichiometric_formula).mass)
                else:
                    alert = ""

                print("{0: <12} # {1: <6} # {2: <7} # {3: <12} # {4: <75} # {5: <125}".format(species_name, species_charge, db_mass, pyvalem_mass, alert, species_inchi))
            except TypeError as e:
                pass
                #print("Missing in Pyvalem : {}, mass is {}, {}".format(species.stoichiometric_formula, Formula(species.stoichiometric_formula).mass, species.inchi))
            except Exception as e:
                print(type(e))
                print(e)
                print("Failed for {}".format(species.stoichiometric_formula))
        


