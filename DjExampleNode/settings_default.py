#
# Default config for a node. When creating your own node, run 'manage.py' to
# build your own settings.py file in the node, then copy&paste variables you need to
# change from this file. Don't edit this file directly. 
#

import sys, os

###################################################
# Basic node setup 
###################################################
# root path of the VAMDC install on your system (should be automatically set)
BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_PATH)
# Path to this node 
NODE_PATH = os.path.dirname(os.path.abspath(__file__))
# Python-path to app folder (usually <yournodename>.node)
NODEPKG= os.path.basename(NODE_PATH)+'.node'
# TAP base url. Must have trailing slash!
TAP_URL = 'http://example.com/YourDBname/tap/'
# Tuple of auto-created admin info for database. Admins are added as tuples (name, email). 
# (note: the trailing ',' is what keeps it a 1-element tuple!)
ADMINS = (('yourname', 'name@mail.net'),) 
MANAGERS = ADMINS

###################################################
# Database connection
# Setting up the database type and information.
# Simplest for testing is sqlite3.
###################################################
DATABASE_ENGINE = 'sqlite3' # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sq$
DATABASE_NAME = 'node.db'   # the path to the db file for sqlite3, the DB-name $
DATABASE_USER = ''             # Not used with sqlite3.
DATABASE_PASSWORD = ''         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used wi$
DATABASE_PORT = ''             # Set to empty string for default. Not used with$

###################################################
# Django components
###################################################
#Copy this field to settings and append the path to
# the node that you want to run.
INSTALLED_APPS = (
    'django.contrib.contenttypes',
#    'django.contrib.sessions',
#    'django.contrib.sites',
#    'django.contrib.admin',
#    'django.contrib.admindocs',
    'DjNode.tapservice',
    NODEPKG
)
# Setup of Django middleware components (shouldn't have to change this))
MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
 #   'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

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
# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(NODE_PATH, 'static/media')
# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = 'http://vamdc.fysast.uu.se:8888/media/'
# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/admin-media/'
# Make this unique, and don't share it with anybody.
SECRET_KEY = '=4nk7k_v3p@gin!bgp*oh2_t@(_hfdvuza27g1&_r4j3(2!+i1'
# Where to load url info from 
ROOT_URLCONF = 'DjVALD.urls'
# Web template locations
TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(BASE_PATH,'DjNode', 'templates'),
)
# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

