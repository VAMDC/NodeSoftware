# Optional:
# Use this file to connect views from views.py in the same
# directory to their URLs.

from django.conf.urls import url, include
#from django.conf import settings

import vamdctap

#urlpatterns =  [
#    url(r'^tap/', include('vamdctap.urls')),
#    ]

urlpatterns = vamdctap.url.urlpatterns
print(urlpatterns)
