"""
WSGI config for Main project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from manage import DEFAULT_SETTINGS_MODULE
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", DEFAULT_SETTINGS_MODULE)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Main.settings")

application = get_wsgi_application()