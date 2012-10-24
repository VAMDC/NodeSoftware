import os
import sys
sys.path.append('/var/www/vamdcdev/')

os.environ['DJANGO_SETTINGS_MODULE'] = 'nodes.jpl.settings'


import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
