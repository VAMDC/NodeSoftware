from django.urls import re_path
from django.conf import settings
import django.views.static
from vamdctap.views import sync, availability, capabilities, tables
#import vamdctap

urlpatterns = [re_path(r'^sync[/]?$', sync),
               # re_path(r'^async/', 'async'),
               re_path(r'^availability[/]?$', availability),
               re_path(r'^capabilities[/]?$', capabilities),
               re_path(r'^tables[/]?$', tables),
               ]

if settings.SERVE_STATIC:
    import django.views.static
    urlpatterns += [re_path(r'^static/(?P<path>.*)$',
                    django.views.static.serve,
                    {'document_root': settings.BASE_PATH+'/static'}),
                    ]

