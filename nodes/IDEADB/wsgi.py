import os
import sys

# EDIT THE FOLLOWING TWO LINES
sys.path.append('/var/opt/vamdcgit/NodeSoftware/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'nodes.IDEADB.settings'


import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
