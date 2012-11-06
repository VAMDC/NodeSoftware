from settings_default import *

#DEBUG = True
DEBUG = False
TRANSLIM = 6000

try:
    INSTALLED_APPS.remove('vald.node')
except:
    pass

NODEPKG='vald.node_atom'
if not 'vald.node_common' in INSTALLED_APPS:
    INSTALLED_APPS.append('vald.node_common')
if not NODEPKG in INSTALLED_APPS:
    INSTALLED_APPS.append(NODEPKG)
#print NODEPKG,INSTALLED_APPS

DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.mysql',
    'NAME': 'vald_atom',
    'USER': 'vald',
    'PASSWORD': 'V@ld',
  },
}
EXAMPLE_QUERIES = [\
    "SELECT ALL WHERE RadTransWavelength > 4000 AND RadTransWavelength < 4000.01",
    "SELECT ALL WHERE AtomSymbol = 'U'",
    "SELECT ALL WHERE ( AtomSymbol = 'Mg' ) AND (RadTransWavelength >= 5100 AND RadTransWavelength <= 5200)",
    "SELECT SPECIES",
    ]
ADMINS = (('Thomas', 'thomas@marquart.se'),)
SERVER_EMAIL = 'vamdc@vald.astro.uu.se'
DEPLOY_URL = 'http://vald.astro.uu.se/atoms-dev/tap/'

LOGGING['handlers']['logfile']['filename'] = '/tmp/atomnode.log'
#LOGGING['handlers']['logfile']['filename'] = '/tmp/test_atomnode.log'
if not DEBUG:
    LOGGING['handlers']['logfile']['level'] = 'INFO'
