from django.conf.urls.defaults import *

urlpatterns = patterns('DjVAMDC',
                       (r'^$', 'vald.views.index'),
                       (r'^tap/', include('DjVAMDC.tapservice.urls')),
                       )
