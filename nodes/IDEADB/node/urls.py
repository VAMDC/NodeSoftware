# Optional:
# Use this file to connect views from views.py in the same
# directory to their URLs.

from django.conf.urls import include, url
from django.conf import settings
from django.contrib import admin

#admin.autodiscover()

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
]

#urlpatterns = patterns(settings.NODENAME+'.node.views',
#                       (r'^$', 'index'),
#                       )
