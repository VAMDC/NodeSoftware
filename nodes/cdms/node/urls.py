# Optional:
# Use this file to connect views from views.py in the same
# directory to their URLs.

from django.conf.urls.defaults import *
from django.conf import settings
#
urlpatterns = patterns(settings.NODENAME+'.node.views',
                       (r'^$', 'index'),
                       (r'^cdms', 'index'),
                       (r'^queryPage', 'queryPage'),                       
                       (r'^queryForm', 'queryForm'),
                       (r'^showResults', 'showResults'),
                       )
