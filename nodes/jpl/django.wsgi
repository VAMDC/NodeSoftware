import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) )

os.environ['DJANGO_SETTINGS_MODULE'] = 'nodes.jpl.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

