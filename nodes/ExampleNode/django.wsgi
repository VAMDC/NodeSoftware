import os
import sys

# EDIT THE FOLLOWING LINES
sys.path.append('/path/to/your/NodeSoftware')
sys.path.append('.')
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'


# No edit below here
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
