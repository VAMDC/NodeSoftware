from settings_default import *

DEBUG = True
#DEBUG = False
TRANSLIM = 6000

INSTALLED_APPS.remove(NODEPKG)
INSTALLED_APPS.append(NODENAME+'.node_common')
NODEPKG=NODENAME+'.node_atom'
INSTALLED_APPS.append(NODEPKG)

DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.mysql',
    'NAME': 'vald_atom',
    'USER': 'vald',
    'PASSWORD': 'V@ld',
  },
}

ADMINS = (('Thomas', 'thomas@marquart.se'),)
EXAMPLE_QUERIES = ['SELECT ALL WHERE RadTransWavelength > 4000 AND RadTransWavelength < 4005',
                   'SELECT ALL WHERE AtomSymbol = U']
SERVER_EMAIL = 'vamdc@vald.astro.uu.se'

LOGGING['handlers']['logfile']['filename'] = '/tmp/atomnode.log'
if not DEBUG:
    LOGGING['handlers']['logfile']['level'] = 'INFO'
