import os
import sys

#sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.append('/var/cdms/v1_0/NodeSoftware/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'nodes.cdms.settings'

#import django.core.handlers.wsgi
#application = django.core.handlers.wsgi.WSGIHandler()
#
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
