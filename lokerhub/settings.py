from __future__ import absolute_import
"""
Django settings for lokerhub project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from django.conf import global_settings
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'tht!tn3cs^(wh%i*8q(1nv49b+=ytcxp@sv^@3&00mx50n-3%m'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = ['.lokerhub.com']

ADMINS = (
    ('LokerHub', 'hello@lokerhub.com'),
)
MANAGERS = ADMINS


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'hub',
    'south',
    'djcelery',
    'kombu.transport.django',
    'djsupervisor',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

AUTHENTICATION_BACKENDS = ('hub.backends.LoginRadiusBackend',) + global_settings.AUTHENTICATION_BACKENDS

TEMPLATE_CONTEXT_PROCESSORS = global_settings.TEMPLATE_CONTEXT_PROCESSORS + (
    'hub.context_processors.LokerHub',
)

ROOT_URLCONF = 'lokerhub.urls'

WSGI_APPLICATION = 'lokerhub.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }

DATABASES = {
    'default': {
        'ENGINE':'django.db.backends.mysql',
        'NAME': 'lokerhubdb',
        'USER': 'lokerhubdbuser',
        'PASSWORD': 'kvPzq2TeAqtR73Z',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'assets', 'static')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'assets', 'media')

# Celery
from celery.schedules import crontab
BROKER_URL = 'django://'
CELERY_RESULT_BACKEND = 'djcelery.backends.database:DatabaseBackend'
CELERYBEAT_SCHEDULE = {
    'check-expired-job': {
        'task': 'hub.tasks.task_periodic_check_jobtime',
        'schedule': crontab(hour=0, minute=0),
    },
}

# Site Domain
SITE_DOMAIN = 'http://lokerhub.com' #'http://localhost:8000'

# Login URL
LOGIN_URL = '/login/'

# Login Radius settings
LRD_API_KEY = 'fec3a884-cdd4-49ed-a9a3-68e314b6277f'
LRD_API_SECRET = '3ad274a8-2155-46a3-a293-6a68ca14ce8d'
LRD_FACEBOOK_AUTH_URL = 'https://lokerhub.hub.loginradius.com/requesthandlor.aspx?apikey=%s&provider=facebook&callback=&scope=' % LRD_API_KEY
LRD_GOOGLE_AUTH_URL = 'https://lokerhub.hub.loginradius.com/requesthandlor.aspx?apikey=%s&provider=google&callback=&scope=' % LRD_API_KEY
LRD_LINKEDIN_AUTH_URL = 'https://lokerhub.hub.loginradius.com/requesthandlor.aspx?apikey=%s&provider=linkedin&callback=&scope=' % LRD_API_KEY

# Indeed Publisher Key
SERVER_IP = '128.199.206.218'
INDEED_PUBLISHER_ID = '1629136956167852'
INDEED_API_URL = 'http://api.indeed.com/ads/apisearch?publisher=%s&q=%s&l=&sort=&radius=&st=&jt=&start=%s&limit=25&fromage=&filter=&latlong=0&co=id&chnl=&userip=%s&useragent=LokerHub&v=2&format=json'
# example usage url : url = INDEED_API_URL % (INDEED_PUBLISHER_ID, 'java developer', SERVER_IP)

LINKEDIN_API_KEY = '7512c1njmlwnr1'

# Twitter API
TWITTER_CONSUMER_KEY = 'snT6SA32WQEvuB7eUwKFw'
TWITTER_CONSUMER_SECRET = 'fkfq9Ufr1dkWWe7nW5CWfQ7uGP4EqSCn2l0rxv0DQtY'
TWITTER_ACCESS_TOKEN = '2384819797-r8iJXjCiWCnyHYtm4iqtG6smUzzm8rkCyJSj0pU'
TWITTER_TOKEN_SECRET = 'EN8gLVfPR8wAJ8SYdL2rWiqFlVRyqBaNRNrqhJFwG02us'

# Cron Key
CRONJOB_KEY = '^*&*!&JGJAGDJAGDAI*(*ADKASUGDA*&A*&ADJHADJGAD'

# Premium fee
PREMIUM_FEE = 100000

# My Bank
BANKS = [
    {'name': 'BCA', 'branch': 'Ubud, Bali', 'an': 'Pande Putu Eka Putra', 'ac': '135.024.2593'} 
]

# Email settings
if DEBUG:
    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True

    EMAIL_HOST_USER = ''
    EMAIL_HOST_PASSWORD = ''
