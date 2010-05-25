from django.conf.urls.defaults import *

urlpatterns = patterns('DjCDMS.cdms.views',
                       (r'^$', 'index'),
                       (r'^tap/sync/','sync'),
                       (r'^tap/','index'),
                       )
