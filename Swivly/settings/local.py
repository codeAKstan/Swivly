from .base import *

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'swivly_db',
        'USER': 'postgres',
        'PASSWORD': '554433',
        'PORT': '5432',
        'HOST': '127.0.0.1',
        'PORT':'5432'
    }
}
