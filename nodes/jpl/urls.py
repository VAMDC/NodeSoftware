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
    (r'^jpl/', include('nodes.jpl.node.urls')),
#    (r'^cdms/static', include('nodes.cdms.node.urls')),
    (r'^mycdmsadmin/', include('nodes.jpl.mycdmsadmin.urls')),
)

if settings.SERVE_STATIC:
    import django.views.static
    urlpatterns += patterns('',
                    (r'^jpl/static/(?P<path>.*)$',
                    django.views.static.serve,
                    {'document_root': settings.BASE_PATH+'/nodes/jpl/static'}),
                    (r'mycdmsadmin/static/(?P<path>.*)$',
                    django.views.static.serve,
                    {'document_root': settings.BASE_PATH+'/nodes/jpl/mycdmsadmin/static'}),                    
                    )

