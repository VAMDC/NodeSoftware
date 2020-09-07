import os
import sys

# EDIT THE FOLLOWING TWO LINES
sys.path.append('/data/VAMDC-NodeSoftware/')
# sys.path.append('/data/VAMDC-NodeSoftware/nodes/KIDA')
os.environ['DJANGO_SETTINGS_MODULE'] = 'nodes.KIDA.settings'


# import django.core.handlers.wsgi
# application = django.core.handlers.wsgi.WSGIHandler()

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
