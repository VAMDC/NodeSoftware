from django.conf.urls.defaults import *
from models import KeyWord
from django.contrib.admin.models import LogEntry

urlpatterns = patterns('django.views.generic.list_detail',
    # Example:
    #(r'^browse/', include('dictionary.browse.urls')),
    (r'^$', 'object_list', {'queryset':KeyWord.objects.all(), 'template_name':'dictionary/index.html'} ),
    (r'^log/', 'object_list', {'queryset':LogEntry.objects.all(), 'template_name':'dictionary/log.html'} ),
)
urlpatterns += patterns('dictionary.browse.views',
    (r'^check/', 'check'),
)
