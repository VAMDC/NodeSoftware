import os
import sys
sys.path.append('/home/tom/py/')
sys.path.append('/home/tom/py/vamdc/')

os.environ['DJANGO_SETTINGS_MODULE'] = 'nodes.vald.settings'


import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
