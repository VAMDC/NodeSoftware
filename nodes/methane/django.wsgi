import os
import sys

# EDIT THE FOLLOWING TWO LINES
sys.path.append('/var/www/NodeSoftware-11.12')
os.environ['DJANGO_SETTINGS_MODULE'] = 'nodes.methane.settings'


import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
