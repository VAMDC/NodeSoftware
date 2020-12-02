#
# Default config for a node. When creating your own node, run 'manage.py' to
# build your own settings.py file in the node, then copy&paste variables you need to
# change from this file. Don't edit this file directly.
#

import sys, os
import datetime

###################################################
# Software and standards version
###################################################
VAMDC_STDS_VERSION = '12.07'
NODESOFTWARE_VERSION = '12.07-github-master'

###################################################
# Basic node setup
###################################################
# root path of the VAMDC install on your system (should be automatically set)
BASE_PATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(BASE_PATH)
sys.path.append(BASE_PATH+'/nodes')
NODENAME = os.path.basename(os.path.dirname(__file__))
NODEPKG = 'node'
NODEVERSION = 1

# Where to load url info from
ROOT_URLCONF = 'urls'

# Tuple of auto-created admin info for database. Admins are added as tuples (name, email).
# (note: the trailing ',' is what keeps it a 1-element tuple!)
ADMINS = (('yourname', 'name@example.com'),)
MANAGERS = ADMINS

EXAMPLE_QUERIES = ['SELECT ALL WHERE ... something',
                   'SELECT ALL WHERE ... something else',
                   ]

LAST_MODIFIED = datetime.date(1911,2,3)

# This turns on/off the serving of static files
# though Django. It is better to let the deployment
# webserver do this, not Django. But it is on
# by default to make things fail-safe.
SERVE_STATIC = True

# MIRROR sites
MIRRORS = []

# Preferred applications that work with the node
VAMDC_APPS = []

###################################################
# Database connection
# Setting up the database type and information.
# Simplest for testing is sqlite3.
###################################################
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'node.db',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

###################################################
# Django components
###################################################
#Copy this field to settings and append the path to
# the node that you want to run.
INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.auth',
#    'django.contrib.sessions',
#    'django.contrib.sites',
#    'django.contrib.admin',
#    'django.contrib.admindocs',
    'django.contrib.staticfiles',
    'vamdctap',
    NODEPKG
]
# Setup of Django middleware components (shouldn't have to change this))
MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
#    'django.contrib.sessions.middleware.SessionMiddleware',
#    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

TEST_RUNNER = 'django.test.runner.DiscoverRunner'

###################################################
# Misc settings
###################################################

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Berlin'
# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'
# Give debug messages
DEBUG = False
# For web templates, use Python traceback instead of Server Error message.
TEMPLATE_DEBUG = DEBUG
# site id number (you shouldn't have to change this)
SITE_ID = 1
# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

###################################################
# Web features
###################################################
#STATIC_URL = '/static/'
# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
#MEDIA_ROOT = os.path.join(BASE_PATH, 'static')
# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
#MEDIA_URL = 'http://vamdc.fysast.uu.se:8888/static/'
# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
#ADMIN_MEDIA_PREFIX = '/admin-media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '=4nk7k_v3p@gin!bgp*oh2_t@(_hfdvuza27g1&_r4j3(2!+i1'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_PATH,'static', 'templates')],
    },
]

# OLD
#TEMPLATE_DIRS = (
#    os.path.join(BASE_PATH,'static', 'templates'),
#)
#TEMPLATE_LOADERS = (
#    'django.template.loaders.filesystem.Loader',
#)

# ALLOW TO SERVE FROM ALL HOSTS
ALLOWED_HOSTS = ['*']

#########################
#  LOGGING
########################
import tempfile
TMPDIR = tempfile.gettempdir()
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(asctime)s %(levelname)s %(message)s'
        },
    },
    'handlers': {
        'null': {
            'level':'DEBUG',
            'class':'logging.NullHandler',
        },
        'console':{
            'level':'WARNING',
            'class':'logging.StreamHandler',
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True,
        },
        'logfile':{
                'level': 'DEBUG',
                'class': 'logging.FileHandler',
                'filename': TMPDIR+'/node.log',
                'formatter': 'simple'
        }
    },
    'loggers': {
        'django': {
            'handlers':['null'],
            'propagate': True,
            'level':'INFO',
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        'vamdc': {
            'handlers': ['console','logfile','mail_admins'],
            'level': 'DEBUG',
        },
        'vamdc.tap': {
            'level': 'DEBUG',
        },
        'vamdc.tap.sql': {
            'level': 'DEBUG',
        },
        'vamdc.tap.generator': {
            'level': 'DEBUG',
        },
        'vamdc.node': {
            'level': 'DEBUG',
        },
        'vamdc.node.queryfu': {
            'level': 'DEBUG',
        },
    }
}

QUERY_STORE_ACTIVE = False
QUERY_STORE_URL = 'https://querystore.vamdc.eu/NotificationListener'
QUERY_STORE_USER_AGENT = 'VAMDC Query store'
