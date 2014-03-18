import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

os.environ['DJANGO_SETTINGS_MODULE'] = 'nodes.cdms.settings'


import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
