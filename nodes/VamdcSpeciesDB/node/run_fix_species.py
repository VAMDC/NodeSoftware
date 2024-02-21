# This is executed only once to update values in vamdc_species table where mass_number == 0 
# and wrongly written inchi before the february 2024 service update
import post_processing as postproc

postproc.fix_species_values()
