#
# VAMDC-node config file
#
# You may customize your setup by copy&pasting the variables you want to
# change from the default config file in nodes/settings_default.py to
# this file. Try to only copy over things you really need to customize
# and do *not* make any changes to settings_defaults.py directly. That
# way you'll always have a sane default to fall back on (also, the
# master file may change with updates).

from settings_default import *

# Comment out the following line once your node goes live.
# As long as this is set to True there will be additional
# logging output and performance will be slower.
DEBUG=True

# Remove this for any other node than the ExampleNode
# It is simply a flag needed to run the tests.
EXAMPLENODE=True

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

###############################################
# Admin information
# You NEED to set a valid email-adress here
# since critical errors will be emailed there.
###############################################
ADMINS = (  ('Admin 1 Name', 'name1@mail.net'),
            ('Admin 2 Name', 'name2@mail.net'),
         )

## The "sent from" email-address that is used
## when the software sends email
#SERVER_EMAIL = 'foo@bar.com'

## Deploy URL
## This overrides the default, in case
## the automatism does not work. Eg. when
## running behind a proxy.
#DEPLOY_URL = 'http://your.server/path/tap/'


###############################################
# Last modified
# This allows to set a global date of last
# change which clients can use to (not) re-run
# a query.
###############################################
#LAST_MODIFIED = datetime.date(1900,1,1)

###############################################
# Example query
# Please comment out the following and adapt it
# to at least one meaningful query for your node.
###############################################
# EXAMPLE_QUERIES = ['SELECT ALL WHERE ... something',
#                    'SELECT ALL WHERE ... something else',
#                   ]

###############################################
# Logging
# You can uncomment the following line and set
# the filename. Unless you do so, the log-file
# is called 'node.log' and resides in your
# systems TMP-directory
###############################################
# LOGGING['handlers']['logfile']['filename'] = '/some/path/mylog.log'

