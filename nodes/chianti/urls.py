#from django.conf.urls.defaults import patterns, include

# Uncomment the next two lines to enable the admin:
#from django.contrib import admin
#admin.autodiscover()

#urlpatterns = patterns('',

    # Uncomment the next line to enable the admin:
    #(r'^admin/', include(admin.site.urls)),
    #(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    #(r'^tap/', include('vamdctap.urls')),
    #(r'', include('node.urls')),

#)
from vamdctap import urls
