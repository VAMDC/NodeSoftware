from settings_default import *

DEBUG = False
DEBUG = True
TRANSLIM = 100000

try:
    INSTALLED_APPS.remove('node')
except:
    pass

NODEPKG='node_atom'
if not 'node_common' in INSTALLED_APPS:
    INSTALLED_APPS.append('node_common')
if not NODEPKG in INSTALLED_APPS:
    INSTALLED_APPS.append(NODEPKG)

DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.mysql',
    'NAME': 'vald_atom',
    'USER': 'vald',
    'PASSWORD': 'V@ld',
  },
}
LAST_MODIFIED = datetime.date(2017,1,24)

EXAMPLE_QUERIES = [\
    "SELECT ALL WHERE RadTransWavelength > 4000 AND RadTransWavelength < 4000.01",
    "SELECT ALL WHERE AtomSymbol = 'U'",
    "SELECT ALL WHERE ( AtomSymbol = 'Mg' ) AND (RadTransWavelength >= 5100 AND RadTransWavelength <= 5200)",
    "SELECT SPECIES",
    ]
ADMINS = (('Thomas', 'thomas@marquart.se'),)
SERVER_EMAIL = 'vamdc@vald.astro.uu.se'
DEPLOY_URL = 'http://vald.astro.uu.se/atoms-dev/tap/'

VAMDC_APPS = [\
    "ivo://vamdc/atomicxsams2html",
    "ivo://vamdc/xsams-mux",
    "ivo://vamdc/xsams2sme",
    "ivo://vamdc/XSAMS-bibtex",
    "ivo://vamdc/xsams-views",
#    "ivo://vamdc/",
#    "ivo://vamdc/",
#    "ivo://vamdc/",
    ]

LOGGING['handlers']['logfile']['filename'] = '/tmp/atomnodeDev.log'
if not DEBUG:
    LOGGING['handlers']['logfile']['level'] = 'INFO'


# Query inspecting as of https://github.com/dobarkod/django-queryinspect
#MIDDLEWARE_CLASSES = (
#    'django.middleware.common.CommonMiddleware',
#    'qinspect.middleware.QueryInspectMiddleware',
#    )
# Whether the Query Inspector should do anything (default: False)
#QUERY_INSPECT_ENABLED = True
# Whether to log the stats via Django logging (default: True)
#QUERY_INSPECT_LOG_STATS = True
# Whether to add stats headers (default: True)
#QUERY_INSPECT_HEADER_STATS = True
# Whether to log duplicate queries (default: False)
#QUERY_INSPECT_LOG_QUERIES = True
# Whether to include tracebacks in the logs (default: False)
#QUERY_INSPECT_LOG_TRACEBACKS = False
# Project root (one or several colon-separated directories, default empty)
#QUERY_INSPECT_TRACEBACK_ROOTS = '/path/to/my/django/project/'
