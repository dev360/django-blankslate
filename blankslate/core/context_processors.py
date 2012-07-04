from django.conf import settings

# Get a bunch of settings
SITE_NAME = getattr(settings, 'SITE_NAME', '')
BASE_URL = getattr(settings, 'BASE_URL', '')



