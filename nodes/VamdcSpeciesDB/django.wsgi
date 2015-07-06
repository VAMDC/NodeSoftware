import os
import sys

# EDIT THE FOLLOWING TWO LINES
sys.path.append('/var/cdms/v1_0/NodeSoftware/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'nodes.VamdcSpeciesDB.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
