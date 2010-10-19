from django.conf.urls.defaults import *
from DjHITRAN.HITRAN import views
from django.conf import settings
#from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns('',
		(r'', include('DjNode.urls')),
		(r'^HITRAN/search_xsec/$', views.search_xsec),
        (r'^node/HITRAN/tap/sync/$', views.sync),
		#(r'^HITRAN/search/$', views.search),
		(r'^HITRAN/media/(?P<path>.*)$', 'django.views.static.serve',
			{'document_root': settings.BASEPATH+'DjHITRAN/media'} ),
		(r'^HITRAN/scripts/(?P<path>.*)$', 'django.views.static.serve',
			{'document_root': settings.BASEPATH+'DjHITRAN/scripts'} ),
)

# Replace the base by your node name and add urls
# if you have custom views.
#urlpatterns + = patterns('DjExampleNode.node.views',
#                       (r'^$', 'index'),
#                       )

