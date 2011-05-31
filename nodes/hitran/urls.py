from django.conf.urls.defaults import *
import settings

# Uncomment the next two lines to enable the admin:
#from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns('',

    # Uncomment the next line to enable the admin:
    #(r'^admin/', include(admin.site.urls)),
    #(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    (r'^tap/', include('vamdctap.urls')),
    (r'^HITRAN/searchapp/results/(?P<filename>.*)$',
            'searchapp.views.serve_file'),
    (r'^HITRAN/', 'searchapp.views.index'),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_PATH}),

    )


