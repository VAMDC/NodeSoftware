from django.conf.urls.defaults import *

urlpatterns = patterns('vamdctap.views',
                       (r'^$', 'index'),
                       (r'^sync[/]?$', 'sync'),
                       #(r'^async/', 'async'),
                       (r'^availability[/]?$', 'availability'),
                       (r'^capabilities[/]?$', 'capabilities'),
                       (r'^tables/', 'tables'),
                       (r'^Tables.xsd$', 'tablesXsd'),
                       (r'^Capabilities.xsd$', 'capabilitiesXsd'),
                       (r'^Capabilities.xsl$', 'capabilitiesXsl'),
                       (r'^Availability.xsl$', 'availabilityXsl'),
                       )
