import os
import sys

# EDIT THE FOLLOWING TWO LINES
sys.path.append('/home/doronin/space/doronin/VAMDC/python/NodeSoftware/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'nodes.VamdcSpeciesDB.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
