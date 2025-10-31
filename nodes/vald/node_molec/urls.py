from importlib import import_module

from django.conf import settings
from django.urls import path

urlpatterns = []

try:
    node_views = import_module(f"{settings.NODENAME}.node.views")
    urlpatterns.append(path("", node_views.index, name="index"))
except (ModuleNotFoundError, AttributeError):
    # Legacy nodes may not ship a landing-page view.
    urlpatterns = []
