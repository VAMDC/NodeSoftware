# Optional:
# Use this file to connect views from views.py in the same
# directory to their URLs.
from django.contrib.auth.views import login, logout

from django.conf.urls.defaults import *
from django.conf import settings

from django.views.decorators.cache import cache_page
#
urlpatterns = patterns(settings.NODENAME+'.node.views',
                       (r'^$', 'index'),
                       (r'^cdms$', 'index'),
                       (r'^home', 'index'),
                       (r'^queryPage', 'queryPage'),                       
                       (r'^queryForm', 'query_form'), 
                       (r'^querySpecies', 'queryspecies'),
                       (r'^html_list/([a-z]{1,20})/$', 'html_list'),
#                       (r'^json_list/([a-z]{1,20})/$', cache_page(60*15)('json_list')),
                       (r'^json_list/([a-z]{1,20})/$', 'json_list'),
                       (r'^selectSpecie2', 'selectSpecie2'),
                       (r'^selectSpecie', 'selectSpecie'),
                       (r'^catalog/(\d{1,5})/$', 'catalog'),
                       (r'^catalog', 'catalog'),
                       (r'^showResults', 'showResults'),
                       (r'^ajaxRequest', 'ajaxRequest'),
#                       (r'^xsams2html', 'xsams2html'),
                       (r'^tools', 'tools'),
                       (r'^general', 'general'),
                       (r'^contact', 'contact'),
                       (r'^help', 'help'),
                       (r'^overview$','specieslist'),
              #         (r'^molecules', 'molecule'),                       
              #         (r'^species/(\d{1,5})/$', 'specie'),                       
                       (r'^getfile/(\d{1,5})/$', 'getfile'),                       
                       (r'^cdms_lite', 'cdms_lite_download'),                       
              #         (r'^references', 'referencelist'),                       
              #         (r'^filters/(\d{1,5})/$', 'filters'),                      
                       (r'^login/$',  login, {'template_name': 'cdmsadmin/login.html'}),
                       (r'^accounts/logout/$', logout, {'template_name': 'cdmsadmin/login.html'}), 
                       )
