# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^basecol/', include('basecol.foo.urls')),
    (r'', include('DjNode.urls')),
    (r'', include('DjBASECOL.bastest.urls')),
    #(r'^node/$', 'DjBASECOL.bastest.views.index'),
    #(r'^node/(?P<ref_id>\d+)/$', 'DjBASECOL.bastest.views.detail'),
    #(r'^node/(?P<ref_id>\d+)/refs/$', 'DjBASECOL.bastest.views.authors'),
    #(r'^node/(?P<ref_id>\d+)/etable/$', 'DjBASECOL.bastest.views.etable'),
    

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    #(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    #(r'^admin/', include(admin.site.urls)),
)
