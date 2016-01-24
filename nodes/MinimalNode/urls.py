from django.conf.urls import patterns, url, include

urlpatterns = patterns('',
    (r'^tap/', include('vamdctap.urls')),
)

handler500 = 'vamdctap.views.tapServerError'
handler404 = 'vamdctap.views.tapNotFoundError'
