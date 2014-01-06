from settings_default import *

DEBUG = False
#DEBUG = True
TRANSLIM = 50000

try:
    INSTALLED_APPS.remove('vald.node')
except:
    pass

NODEPKG='vald.node_atom'
if not 'vald.node_common' in INSTALLED_APPS:
    INSTALLED_APPS.append('vald.node_common')
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
LAST_MODIFIED = datetime.date(2012,12,18)

EXAMPLE_QUERIES = [\
    "SELECT ALL WHERE RadTransWavelength > 4000 AND RadTransWavelength < 4000.01",
    "SELECT ALL WHERE AtomSymbol = 'U'",
    "SELECT ALL WHERE ( AtomSymbol = 'Mg' ) AND (RadTransWavelength >= 5100 AND RadTransWavelength <= 5200)",
    "SELECT SPECIES",
    ]
ADMINS = (('Thomas', 'thomas@marquart.se'),)
SERVER_EMAIL = 'vamdc@vald.astro.uu.se'
DEPLOY_URL = 'http://vald.astro.uu.se/atoms-12.07/tap/'

LOGGING['handlers']['logfile']['filename'] = '/tmp/atomnode12.07.log'
if not DEBUG:
    LOGGING['handlers']['logfile']['level'] = 'INFO'
