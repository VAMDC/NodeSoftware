from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Uncomment the next line to enable the admin:
    #(r'^admin/', include(admin.site.urls)),
    #(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # the TAP urls
    (r'^tap/', include('DjNode.tapservice.urls')),

    # the basic node urls, overwrite this or add your app below
    (r'', include('DjNode.node.urls')),
    
)
