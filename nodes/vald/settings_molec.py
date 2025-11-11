from settings_default import *

DEBUG = False
DEBUG = True
TRANSLIM = 200000
QUERY_STORE_ACTIVE = False
SERVE_STATIC = False

NODEPKG = 'node_molec'
INSTALLED_APPS = ['vamdctap', 'node_common', NODEPKG]

DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': 'vald_molec.sqlite',
  },
}
LAST_MODIFIED = datetime.date(2025,10,22)
NODEVERSION = LAST_MODIFIED.isoformat()

EXAMPLE_QUERIES = [\
    "SELECT ALL WHERE RadTransWavelength > 4000 AND RadTransWavelength < 4000.01",
    "SELECT SPECIES",
    ]
ADMINS = (('Thomas', 'thomas.marquart@astro.uu.se'),)
SERVER_EMAIL = 'thomas.marquart@astro.uu.se'
DEPLOY_URL = 'http://localhost:8000/tap/'

VAMDC_APPS = [\
    "ivo://vamdc/xsams-mux",
    "ivo://vamdc/xsams2sme",
    "ivo://vamdc/XSAMS-bibtex",
    "ivo://vamdc/xsams-views",
    ]

LOGGING['handlers']['logfile']['filename'] = 'molec.log'
if not DEBUG:
    LOGGING['handlers']['logfile']['level'] = 'INFO'


#LOGGING['loggers']['django.db.backends'] = {
#      'handlers': ['console', 'logfile'],
#      'level': 'DEBUG',
#      'propagate': False,
#  }

