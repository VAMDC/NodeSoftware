#~ from django.conf.urls.defaults import *
from django.conf.urls import url, include

# Uncomment the next two lines to enable the admin:
#from django.contrib import admin
#admin.autodiscover()

urlpatterns =  [
    url(r'^tap/', include('vamdctap.urls')),
]
handler500 = 'vamdctap.views.tapServerError'
handler404 = 'vamdctap.views.tapNotFoundError'
