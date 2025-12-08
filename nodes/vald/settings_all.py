from settings_default import *

DEBUG = False
#DEBUG = True
TRANSLIM = 200000
QUERY_STORE_ACTIVE = True
SERVE_STATIC = False

NODEPKG = 'node'
INSTALLED_APPS = ['vamdctap', NODEPKG]

DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': 'vald_all.sqlite',
  },
}
LAST_MODIFIED = datetime.date(2025,11,28)
NODEVERSION = LAST_MODIFIED.isoformat()

EXAMPLE_QUERIES = [\
    "SELECT ALL WHERE RadTransWavelength > 4000 AND RadTransWavelength < 4000.01",
    "SELECT ALL WHERE AtomSymbol = 'U'",
    "SELECT ALL WHERE ( AtomSymbol = 'Mg' ) AND (RadTransWavelength >= 5100 AND RadTransWavelength <= 5200)",
    "SELECT SPECIES",
    ]
ADMINS = (('Thomas', 'thomas.marquart@astro.uu.se'),)
SERVER_EMAIL = 'thomas.marquart@astro.uu.se'
DEPLOY_URL = 'https://vald.astro.uu.se/vamdc-all/tap/'

VAMDC_APPS = [\
    "ivo://vamdc/atomicxsams2html",
    "ivo://vamdc/xsams-mux",
    "ivo://vamdc/xsams2sme",
    "ivo://vamdc/XSAMS-bibtex",
    "ivo://vamdc/xsams-views",
    ]

LOGGING['handlers']['logfile']['filename'] = 'node_all.log'
if not DEBUG:
    LOGGING['handlers']['logfile']['level'] = 'INFO'


#LOGGING['loggers']['django.db.backends'] = {
#      'handlers': ['console', 'logfile'],
#      'level': 'DEBUG',
#      'propagate': False,
#  }

import subprocess
def get_git_commit():
    try:
        return subprocess.check_output(
            ['git', 'rev-parse', '--short', 'HEAD'],
            stderr=subprocess.DEVNULL
        ).decode('ascii').strip()
    except Exception:
        return 'unknown'

NODESOFTWARE_VERSION = get_git_commit()
