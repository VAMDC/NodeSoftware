from django.conf.urls import  url, include
from django.contrib import admin
import vamdctap.urls
from node import urls as node_urls

# Uncomment the next two lines to enable the admin:
#from django.contrib import admin
#admin.autodiscover()

urlpatterns = [

    # Uncomment the next line to enable the admin:
    #(r'^admin/', include(admin.site.urls)),
    #(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    #~ url(r'^admin/', include(admin.site.urls)),

    url(r'^tap/', include('vamdctap.urls')),
    
    url(r'', include(node_urls)),

]

handler500 = 'vamdctap.views.tapServerError'
handler404 = 'vamdctap.views.tapNotFoundError'
