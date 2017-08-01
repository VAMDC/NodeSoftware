import os
import sys

# EDIT THE FOLLOWING TWO LINES
sys.path.append('/var/opt/vamdc/NodeSoftware/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'nodes.IDEADB.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
