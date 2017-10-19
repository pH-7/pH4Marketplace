"""
WSGI config for marketplace project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application
from whitenoise.django import DjangoWhiteNoise

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "marketplace.settings")

application = get_wsgi_application()


# Use whitenoise to allow the app serving its own static files on Heroku
application = DjangoWhiteNoise(application)
