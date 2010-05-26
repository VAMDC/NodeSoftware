from django.conf.urls.defaults import *

urlpatterns = patterns('DjVAMDC.tapservice.views',
                       (r'^$', 'index'),
                       (r'^sync/', 'sync'),
                       (r'^async/', 'async'),
                       (r'^availability/', 'availability'),
                       (r'^capabilities/', 'capabilities'),
                       (r'^/tables', 'tables'),
                       #(r'^/', ''),
                       #(r'^/', ''),
                       )
