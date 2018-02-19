# Optional:
# Use this file to connect views from views.py in the same
# directory to their URLs.
from django.conf.urls import  url, include
#from django.conf.urls.defaults import *
#from django.conf import settings

from node.views import NodeSpeciesView

urlpatterns = [
    url(r'^view/',NodeSpeciesView.as_view()),
]
