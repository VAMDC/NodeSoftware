from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^tap/', include('vamdctap.urls')),
)

handler500 = 'vamdctap.views.tapServerError'
handler404 = 'vamdctap.views.tapNotFoundError'
