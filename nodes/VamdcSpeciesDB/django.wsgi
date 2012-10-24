import os
import sys

# EDIT THE FOLLOWING TWO LINES
sys.path.append('/var/cdms/v1_0/NodeSoftware/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'nodes.VamdcSpeciesDB.settings'


import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
