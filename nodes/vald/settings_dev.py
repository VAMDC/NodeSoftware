from settings_default import *

DEBUG = False
DEBUG = True
TRANSLIM = 100000
QUERY_STORE_ACTIVE = False

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
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': 'vald_dev.sqlite',
  },
}
LAST_MODIFIED = datetime.date(2020,1,24)
NODEVERSION = LAST_MODIFIED.isoformat()

EXAMPLE_QUERIES = [\
    "SELECT ALL WHERE RadTransWavelength > 4000 AND RadTransWavelength < 4000.01",
    "SELECT ALL WHERE AtomSymbol = 'U'",
    "SELECT ALL WHERE ( AtomSymbol = 'Mg' ) AND (RadTransWavelength >= 5100 AND RadTransWavelength <= 5200)",
    "SELECT SPECIES",
    ]
ADMINS = (('Thomas', 'thomas@marquart.se'),)
SERVER_EMAIL = 'vamdc@vald.astro.uu.se'
DEPLOY_URL = 'http://localhost:8000/tap/'
STATIC_URL = '/static/'

VAMDC_APPS = [\
    "ivo://vamdc/atomicxsams2html",
    "ivo://vamdc/xsams-mux",
    "ivo://vamdc/xsams2sme",
    "ivo://vamdc/XSAMS-bibtex",
    "ivo://vamdc/xsams-views",
    ]

LOGGING['handlers']['logfile']['filename'] = 'devnode.log'
if not DEBUG:
    LOGGING['handlers']['logfile']['level'] = 'INFO'

LOGGING['loggers']['django.db.backends'] = {
      'handlers': ['console', 'logfile'],
      'level': 'DEBUG',
      'propagate': False,
  }

