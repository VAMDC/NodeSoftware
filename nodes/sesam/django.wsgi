import os
import sys

# EDIT THE FOLLOWING TWO LINES
sys.path.append('/home/tom/py/vamdc/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'nodes.YourNode.settings'


import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
