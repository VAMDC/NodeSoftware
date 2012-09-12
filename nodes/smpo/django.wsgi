import os
import sys

# EDIT THE FOLLOWING TWO LINES
sys.path.append('/home2/NodeSoftware/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'nodes.smpo.settings'


import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
