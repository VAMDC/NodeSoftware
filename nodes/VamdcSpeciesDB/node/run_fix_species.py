import util

#Add path to settings.py to system path
util.append_base_path(2)

#Initialize django
import django
django.setup()

import post_processing as postproc

postproc.fix_species_values()
