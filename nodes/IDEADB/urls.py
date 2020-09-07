from django.conf.urls import url, include

#we need this to use djangos default views
from django.views.generic import ListView, DetailView
from node.views import *
from node.models import *
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^tap/', include('vamdctap.urls')),
    url(r'^view/$', ListView.as_view(model=Energyscan)),
    url(r'^compare/$', ListView.as_view(model=Energyscan,template_name="energyscan_compare_list.html")),
    url(r'^compare/(\d+)/$', ListView.as_view(model=Energyscan)),
    url(r'^view/(\d+)/$', show_energyscan),
    url(r'^compare/(\d+)/(\d+)/$', compare_energyscan),
    url(r'^contact/$', contact),
    url(r'^export/(\d+)/$', export_ascii),
    url(r'^species/$',ListView.as_view(model=Species)),
]

handler500 = 'vamdctap.views.tapServerError'
handler404 = 'vamdctap.views.tapNotFoundError'
