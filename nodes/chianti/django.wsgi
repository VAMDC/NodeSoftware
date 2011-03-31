import os
import sys
sys.path.append('/VAMDC/NodeSoftware')

os.environ['DJANGO_SETTINGS_MODULE'] = 'nodes.YourNode.settings'


import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
