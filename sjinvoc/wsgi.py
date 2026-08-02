"""
WSGI config for sjinvoc project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
"""

import os
import sys

PROJECT_ROOT = "/home/sjinvoc/sjinvoc"

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

#os.environ["DJANGO_SETTINGS_MODULE"] = "sjinvoc.settings.production"
env = os.getenv("DJANGO_ENV", "development")
os.environ["DJANGO_SETTINGS_MODULE"] =  "sjinvoc.settings.local" if env == "development" else f"sjinvoc.settings.{env}"

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

