from django.conf.urls import url
from django.urls import path
from django.conf import settings
import django.views.static
from vamdctap.views import sync, asynch, availability, capabilities, tables, job, result, jobs, form

urlpatterns = [url(r'^sync[/]?$', sync),
               url(r'^async[/]?$', asynch),
               url(r'^availability[/]?$', availability),
               url(r'^capabilities[/]?$', capabilities),
               url(r'^tables[/]?$', tables),
               path('async/jobs/<id>', job),
               path('async/jobs/<id>/result', result),
               path('async/jobs', jobs),
               path('async/form', form)
               ]

if settings.SERVE_STATIC:
    import django.views.static
    urlpatterns += [url(r'^static/(?P<path>.*)$',
                    django.views.static.serve,
                    {'document_root': settings.BASE_PATH+'/static'}),
                    ]

