import os

from django.core.asgi import get_asgi_application


os.environ.setdefault(key="DJANGO_SETTINGS_MODULE", value="config.settings")

application = get_asgi_application()
