from django.conf.urls.defaults import *

# Replace the base by your node name
urlpatterns = patterns('DjNode.node.views',
                       (r'^$', 'index'),
                       )
