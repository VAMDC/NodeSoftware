import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings_atom")

from django.core.asgi import get_asgi_application

application = get_asgi_application()
