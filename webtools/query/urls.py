from django.conf.urls.defaults import *

urlpatterns = patterns('portal.query.views',
                       (r'^$', 'index'),
                       (r'^query/$', 'query'),
                       (r'^sqlquery/$', 'sqlquery'),
                       (r'^results/(?P<qid>\w+)/$', 'results'),
                       
)
