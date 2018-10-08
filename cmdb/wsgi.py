"""
WSGI config for AppWorkOrder project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""
import os

from django.core.wsgi import get_wsgi_application

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APP_NAME = BASE_DIR.rsplit("/", 1)[-1]
DEV = os.environ.get("ENV")
settings = "{}.settings".format(APP_NAME)
if DEV == "PRO":
    settings = "{}.settings_pro".format(APP_NAME)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings)

application = get_wsgi_application()