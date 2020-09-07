from django.conf.urls.defaults import patterns, url, include
from django.conf import settings
import django.views.static

urlpatterns = patterns('vamdctap.views',
                       #(r'^$', 'index'),
                       (r'^sync[/]?$', 'sync'),
                       #(r'^async/', 'async'),
                       (r'^availability[/]?$', 'availability'),
                       (r'^capabilities[/]?$', 'capabilities'),
                       (r'^tables[/]?$', 'tables'),
                       )

if settings.SERVE_STATIC:
    import django.views.static
    urlpatterns += patterns('',
                    (r'^static/(?P<path>.*)$',
                    django.views.static.serve,
                    {'document_root': settings.BASE_PATH+'/static'}),
                    )

