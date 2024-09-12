import os, logging

from .base import *

import dj_database_url # postgre db_url


#  debug is true in staging environment
DEBUG = True

# installed apps for prod only
INSTALLED_APPS += [

]

# read secret key from environment variable
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")

# stripe api keys
STRIPE_SECRET_KEY = os.environ.get("STRIPE_SECRET_KEY")
STRIPE_PUBLISHABLE_KEY = os.environ.get("STRIPE_PUBLISHABLE_KEY")

# paystack api keys
PAYSTACK_SECRET_KEY = os.environ.get("PAYSTACK_SECRET_KEY")
PAYSTACK_PUBLIC_KEY = os.environ.get("PAYSTACK_PUBLIC_KEY")

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases
# set to use postgre backend in production
DATABASES['default'] = dj_database_url.parse( os.environ.get("DATABASE_URL"),
                                                 conn_max_age=600)