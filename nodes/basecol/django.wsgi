# this is currently for a test-setup on thomas' server
# feel free to change it or add another that suits your
# deployment

import os
import sys
sys.path.append('/home/tom/py/')
sys.path.append('/home/tom/py/vamdc/')

os.environ['DJANGO_SETTINGS_MODULE'] = 'DjBASECOL.settings'


import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
