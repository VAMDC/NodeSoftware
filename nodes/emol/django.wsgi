import os
import sys

# EDIT THE FOLLOWING TWO LINES
# Current values reflect preliminary deployment of emol in Cambridge.
sys.path.append('/vamdc/dev/NodeSoftware')
os.environ['DJANGO_SETTINGS_MODULE'] = 'nodes.emol.settings'


import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
