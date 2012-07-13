import os
import sys

# EDIT THE FOLLOWING TWO LINES
sys.path.append('/var/www/NodeSoftware_dev')
os.environ['DJANGO_SETTINGS_MODULE'] = 'nodes.methane.settings'


import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
