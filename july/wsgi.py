"""
WSGI config for july project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "july.settings")

application = get_wsgi_application()
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
staticfiles = os.path.join(BASE_DIR, "staticfiles")
application = WhiteNoise(application, root=staticfiles)
