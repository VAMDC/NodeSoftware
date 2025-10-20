from importlib import import_module

from django.conf import settings
from django.urls import path

urlpatterns = []

try:
    node_views = import_module(f"{settings.NODEPKG}.views")
    urlpatterns.append(path("", node_views.index, name="index"))
except (ModuleNotFoundError, AttributeError):
    # Most nodes expose TAP endpoints only; no landing page view available.
    urlpatterns = []
