from django.conf.urls.defaults import *
from django.conf import settings

urlpatterns = patterns(settings.NODENAME+'.node.views',
                       (r'^$', 'index'),
                       )
