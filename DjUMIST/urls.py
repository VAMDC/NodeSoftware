from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    # Uncomment the next line to enable the admin:
    #(r'^admin/', include(admin.site.urls)),
    #(r'^admin/doc/', include('django.contrib.admindocs.urls')),


    (r'', include('DjNode.urls')),
    #(r'^tap/', include('DjVAMDC.tapservice.urls')),
    (r'', include('DjUMIST.umist.urls')),

)
