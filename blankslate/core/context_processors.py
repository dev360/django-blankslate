from django.conf import settings

# Get a bunch of settings
SITE_NAME = getattr(settings, 'SITE_NAME', '')
BASE_URL = getattr(settings, 'BASE_URL', '')
USE_CDN = getattr(settings, 'USE_CDN', False)

def global_settings(request):
    """
    Context processor for global settings that need
    to be in the context of every view
    """
    return {
        'SITE_NAME': SITE_NAME,
        'BASE_URL': BASE_URL,
        'USE_CDN': USE_CDN,
    }
