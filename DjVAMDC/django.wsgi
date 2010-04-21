import os
import sys
sys.path.append('/home/tom/py/')
sys.path.append('/home/tom/py/vamdc/')
sys.path.append('/home/tom/py/vamdc/DjVAMDC')

os.environ['DJANGO_SETTINGS_MODULE'] = 'DjVAMDC.settings'


import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()