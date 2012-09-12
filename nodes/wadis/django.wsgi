import os
import sys

# EDIT THE FOLLOWING TWO LINES
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
os.environ['DJANGO_SETTINGS_MODULE'] = 'nodes.' + os.path.basename(os.path.dirname(__file__)) + '.settings'


import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
