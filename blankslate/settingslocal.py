ENVIRONMENT = 'dev'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'blankslate',                      # Or path to database file if using sqlite3.
        'USER': 'blankslate',                      # Not used with sqlite3.
        'PASSWORD': 'blankslate',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}


# Change this secret key for each environment.
SECRET_KEY = 'z+@xf!gwjjclm$z1hhi!@p@46f6yn_c)t+)_zpx8zo$#(v$n(l'

MEDIA_URL = 'http://development.blankslate.com:8000/media/'

#
# Email settings - assuming gmail.
#
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = '587'
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = True
SERVER_EMAIL = EMAIL_HOST_USER


#
# Admin settings
#
ADMINS = (
    (EMAIL_HOST_USER, EMAIL_HOST_USER),
)
MANAGERS = ADMINS

