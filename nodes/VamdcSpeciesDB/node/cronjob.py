import sys
import os
import traceback
import util

#Add path to settings.py to system path
util.append_base_path(2)

#Initialize django
import django
import settings
django.setup()

from node.models import *
from node.InchiInfo import InchiInfo
import node
from  node.models import VamdcDictAtoms
import node.import_functions as update
import post_processing as postproc


#Do the work on database
print ("### update nodes")
update.update_nodes()       #Search for new nodes in the registry & update registered ones
print ("### query actives nodes")
update.query_active_nodes() #Update species for nodes that are marked active

postproc.check_deprecated_species()
postproc.fill_search_table()