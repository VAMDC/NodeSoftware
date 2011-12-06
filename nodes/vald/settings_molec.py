from settings_default import *

DEBUG = True
#DEBUG = False
TRANSLIM = 6000

INSTALLED_APPS.remove(NODEPKG)
INSTALLED_APPS.append(NODENAME+'.node_common')
NODEPKG=NODENAME+'.node_molec'
INSTALLED_APPS.append(NODEPKG)

DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.mysql',
    'NAME': 'vald_molec',
    'USER': 'vald',
    'PASSWORD': 'V@ld',
  },
}

ADMINS = (('Thomas', 'thomas@marquart.se'),)
EXAMPLE_QUERIES = []
SERVER_EMAIL = 'vamdc@vald.astro.uu.se'

LOGGING['handlers']['logfile']['filename'] = '/tmp/molecnode.log'
if not DEBUG:
    LOGGING['handlers']['logfile']['level'] = 'INFO'
