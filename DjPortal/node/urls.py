from django.conf.urls.defaults import *

urlpatterns = patterns('DjVAMDC.node.views',
                       (r'^$', 'index'),
                       (r'^vald/',include('DjVAMDC.vald.urls')),
)
