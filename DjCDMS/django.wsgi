import os
import sys
sys.path.append('/home/endres/Projects/vamdc/')

os.environ['DJANGO_SETTINGS_MODULE'] = 'DjCDMS.settings'


import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
