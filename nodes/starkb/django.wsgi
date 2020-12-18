import os
import sys
import site

# EDIT THE FOLLOWING TWO LINES
os.environ['DJANGO_SETTINGS_MODULE'] = 'nodes.starkb.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()



