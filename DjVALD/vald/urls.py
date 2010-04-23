from django.conf.urls.defaults import *

urlpatterns = patterns('DjVALD.vald.views',
                       (r'^$', 'index'),
                       (r'^tap/sync/','sync'),
                       (r'^tap/','index'),
                       )
