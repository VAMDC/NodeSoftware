import os
import sys
import site


# Add the app's directory to the PYTHONPATH
sys.path.append('/home/vamdc/NodeSoftware')
sys.path.append('/home/vamdc/NodeSoftware/nodes')
sys.path.append('/home/vamdc/NodeSoftware/nodes/VamdcSpeciesDB')
os.environ['DJANGO_SETTINGS_MODULE'] = 'nodes.VamdcSpeciesDB.settings'

# Activate your virtual env
activate_env=os.path.expanduser("/home/vamdc/.virtualenvs/django1.10/bin/activate_this.py")
execfile(activate_env, dict(__file__=activate_env))

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()


