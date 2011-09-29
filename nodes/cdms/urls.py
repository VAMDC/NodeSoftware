from django.conf.urls.defaults import *
from django.conf import settings

# Uncomment the next two lines to enable the admin:
#from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns('',

    # Uncomment the next line to enable the admin:
    #(r'^admin/', include(admin.site.urls)),
    #(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    (r'^tap/', include('vamdctap.urls')),
#    (r'^cdms/', include('cdms.urls')),
    (r'^cdms/', include('nodes.cdms.node.urls')),
#    (r'^cdms/static', include('nodes.cdms.node.urls')),
)

if settings.SERVE_STATIC:
    import django.views.static
    urlpatterns += patterns('',
                    (r'^cdms/static/(?P<path>.*)$',
                    django.views.static.serve,
                    {'document_root': settings.BASE_PATH+'/nodes/cdms/static'}),
                    )

