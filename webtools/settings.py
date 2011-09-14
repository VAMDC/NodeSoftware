
DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Thomas Marquart', 'thomas@marquart.se'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'webtools.db',
    }
}

ROOT_URLCONF = 'urls'
TEMPLATE_DIRS = (
    '/home/tom/py/vamdc/static/templates',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.admindocs',
#    'query',
    'xsams2sme',
)

MEDIA_ROOT='/tmp/webtools'
MEDIA_URL='http://vamdc.tmy.se/webtool-files/'
TIME_ZONE = 'Europe/Stockholm'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = False
ADMIN_MEDIA_PREFIX = '/admin-media/'
SECRET_KEY = '=4ne456erg5_v3p@gin!bgp*oh2_t@(_hfdsfgew5y74!!za27g1&_r4j3(2!+i1'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)
