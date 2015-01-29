from django.conf.urls import patterns, url, include

#we need this to use djangos default views
from django.views.generic import ListView, DetailView
from node.views import *
from node.models import *
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    (r'^tap/', include('vamdctap.urls')),
    (r'^view/$', ListView.as_view(model=Energyscan)),
    (r'^compare/$', ListView.as_view(model=Energyscan,template_name="energyscan_compare_list.html")),
    (r'^compare/(\d+)/$', ListView.as_view(model=Energyscan)),
    (r'^view/(\d+)/$', 'node.views.show_energyscan'),
    (r'^compare/(\d+)/(\d+)/$', 'node.views.compare_energyscan'),
    (r'^contact/$', 'node.views.contact'),
    (r'^export/(\d+)/$', 'node.views.export_ascii'),
    (r'^species/$',ListView.as_view(model=Species)),
)

handler500 = 'vamdctap.views.tapServerError'
handler404 = 'vamdctap.views.tapNotFoundError'
