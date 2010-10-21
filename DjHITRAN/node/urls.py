from django.conf.urls.defaults import *
from DjHITRAN.node import views
from django.conf import settings
#from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns('DjHITRAN.node.views',
		#(r'^HITRAN/search_xsec/$', views.search_xsec),
		#(r'^HITRAN/search/$', views.search),
		#(r'^HITRAN/media/(?P<path>.*)$', 'django.views.static.serve',
		#	{'document_root': settings.BASEPATH+'DjHITRAN/media'} ),
		#(r'^HITRAN/scripts/(?P<path>.*)$', 'django.views.static.serve',
		#	{'document_root': settings.BASEPATH+'DjHITRAN/scripts'} ),
                (r'^$', 'index'),
                (r'^tap/sync/', 'sync'),
)

# Replace the base by your node name and add urls
# if you have custom views.
#urlpatterns + = patterns('DjExampleNode.node.views',
#                       (r'^$', 'index'),
#                       )

