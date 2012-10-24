#!/usr/bin/env python
""" Set up the node. A first startup consists of giving the command 
'python manage'. This will create an empty settings file. Copy&paste 
variables you want to change from settings_default.py to setup your 
node. Next define your models. You'll need to add the folder containing 
the 'models' directory to the INSTALLED_APPS tuple at least. Don't edit 
settings_default.py directly. Next run 'python manage.py syncdb'. This 
will read your settings file and create an empty database using your 
models. If you change the models you need to run syncdb again. """

import sys
import os
import traceback

# Tack on the vamdc root directory to the python path.
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

_CREATED_SETTINGS = False    

if not os.path.exists('settings.py'):
    # If settings.py doesn't already exist, create it
    string = "-"*50 + "\n Welcome to the VAMDC node setup."
    string += "\n\n Created a fresh settings.py file for you."
    print string
    settings_file = open('settings.py', 'w')
    _CREATED_SETTINGS = True
    string = \
    """#
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
DEBUG=True

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

#########################################
# Admin information
#########################################
ADMINS = (\
            ('Admin 1 Name', 'name1@mail.net'),
            ('Admin 2 Name', 'name2@mail.net'),
        )

"""
    settings_file.write(string)
    settings_file.close()
    
# Settings file created or already existed. Test it.
    
try:
    import settings
except Exception:
    string = "\n" + traceback.format_exc()
    string += \
"""
Error: Couldn't import the file 'settings.py' in the directory
containing %r. There can be two reasons for this:
  1) You moved your settings.py elsewhere. In that case you need to run
     django-admin.py, passing it the true location of your settings module.
  2) The settings module is where it's supposed to be, but an exception
     was raised when trying to load it. Review the traceback above to
     resolve the problem, then try again. \n"""
    sys.stderr.write(string % __file__)
    sys.exit(1)

# At this point we have an imported settings module, although it may be empty.            
if __name__ == "__main__":
    if _CREATED_SETTINGS:
        string =  "\n Edit your new settings.py file as needed, then run\n"
        string += " 'python manage syncdb'.\n"
        string += "-"*50
        print string
        sys.exit()
    # Run the django setup using our settings file.
    from django.core.management import execute_manager
    #from xml.sax import saxutils
    execute_manager(settings)
