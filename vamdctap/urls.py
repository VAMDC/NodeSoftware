from django.conf.urls import url, include
from django.conf import settings
import django.views.static
from vamdctap.views import sync, availability, capabilities, tables
#import vamdctap

urlpatterns = [url(r'^sync[/]?$', sync),
               #(r'^async/', 'async'),
               url(r'^availability[/]?$', availability),
               url(r'^capabilities[/]?$', capabilities),
               url(r'^tables[/]?$', tables),
               ]

if settings.SERVE_STATIC:
    import django.views.static
    urlpatterns += [url(r'^static/(?P<path>.*)$',
                    django.views.static.serve,
                    {'document_root': settings.BASE_PATH+'/static'}),
                    ]

