from django.conf.urls.defaults import *
from models import KeyWord

urlpatterns = patterns('django.views.generic.list_detail',
    # Example:
    #(r'^browse/', include('dictionary.browse.urls')),
    (r'^$', 'object_list', {'queryset':KeyWord.objects.all(), 'template_name':'dictionary/index.html'} )
)
