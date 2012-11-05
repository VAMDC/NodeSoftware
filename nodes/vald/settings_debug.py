from settings_default import *

DEBUG = True
TRANSLIM = 6000
print "BASE_PATH:",BASE_PATH
INSTALLED_APPS.remove(NODEPKG)
INSTALLED_APPS.append(NODENAME+'.node_common')
NODEPKG=NODENAME+'.node_atom'
INSTALLED_APPS.append(NODEPKG)

DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.mysql',
    'NAME': 'vald_atom_test',
    'USER': 'vald',
    'PASSWORD': 'V@ld',
  },
  'valdx-innodb': {
    'ENGINE': 'django.db.backends.mysql',
    'NAME': 'valdx',
    'USER': 'vald',
    'PASSWORD': 'V@ld',
#    'OPTIONS': {
#           "init_command": "SET storage_engine=INNODB",
#    }
  },
  'valdx': {
    'ENGINE': 'django.db.backends.mysql',
    'NAME': 'valdx',
    'USER': 'vald',
    'PASSWORD': 'V@ld',
  },
  'test': {
    'ENGINE': 'django.db.backends.mysql',
    'NAME': 'test',
    'USER': 'vald',
    'PASSWORD': 'V@ld',
  },
  'memory': {
    'ENGINE': 'django.db.backends.mysql',
    'NAME': 'vald',
    'USER': 'vald',
    'PASSWORD': 'V@ld',
    'OPTIONS': {
           "init_command": "SET storage_engine=MEMORY",
    }
  },
  'sqlite': {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': 'vald.db',
  }

}

LOGGING['handlers']['logfile']['filename'] = '/tmp/node_debug.log'

ADMINS = (('Thomas', 'thomas@marquart.se'),)
#LOGGING['handlers']['logfile']['filename'] = '/tmp/mylog.log'
EXAMPLE_QUERIES = ['SELECT ALL WHERE RadTransWavelength > 4000 AND RadTransWavelength < 4005',
                   'SELECT ALL WHERE AtomSymbol = U']
SERVER_EMAIL = 'vamdc@vald.astro.uu.se'

