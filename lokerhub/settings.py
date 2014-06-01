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

ALLOWED_HOSTS = []

ADMINS = (
    # ('LokerHub', 'hello@lokerhub.com'),
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
    'easy_thumbnails',
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

DATABASES = {
    'default': {
        'ENGINE':'django.db.backends.mysql',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Makassar'
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
from celery.schedules import timedelta, crontab
BROKER_URL = 'django://'
CELERY_RESULT_BACKEND = 'djcelery.backends.database:DatabaseBackend'
CELERYBEAT_SCHEDULE = {
    'check-expired-job': {
        'task': 'hub.tasks.task_periodic_check_jobtime',
        'schedule': timedelta(seconds=3600), #run every hour
    },
    'tweet-todays-job': {
        'task': 'hub.tasks.task_tweet_todays_job',
        # 'schedule': timedelta(seconds=10),
        'schedule': crontab(minute=0, hour='19'), #run on 7am in the morning
    },
}

# Site Domain
SITE_DOMAIN = 'http://localhost:8000'

# Login URL
LOGIN_URL = '/login/'

# Login Radius settings
LRD_API_KEY = ''
LRD_API_SECRET = ''

# Indeed Publisher Key
SERVER_IP = ''
INDEED_PUBLISHER_ID = ''
INDEED_API_URL = 'http://api.indeed.com/ads/apisearch?publisher=%s&q=%s&l=&sort=&radius=&st=&jt=&start=%s&limit=25&fromage=&filter=&latlong=0&co=id&chnl=&userip=%s&useragent=LokerHub&v=2&format=json'
# example usage url : url = INDEED_API_URL % (INDEED_PUBLISHER_ID, 'java developer', SERVER_IP)

LINKEDIN_API_KEY = ''

# Twitter API
TWITTER_CONSUMER_KEY = ''
TWITTER_CONSUMER_SECRET = ''
TWITTER_ACCESS_TOKEN = ''
TWITTER_TOKEN_SECRET = ''

BITLY_ACCESS_TOKEN = ''

# Cron Key
CRONJOB_KEY = ''

# Premium fee
PREMIUM_FEE = 0

# My Bank
BANKS = []

# Google analitics
GOOGLE_ANALYTIC_CODE = ''

try:
    from .local_settings import *
except ImportError:
    pass


LRD_FACEBOOK_AUTH_URL = 'https://lokerhub.hub.loginradius.com/requesthandlor.aspx?apikey=%s&provider=facebook&callback=&scope=' % LRD_API_KEY
LRD_GOOGLE_AUTH_URL = 'https://lokerhub.hub.loginradius.com/requesthandlor.aspx?apikey=%s&provider=google&callback=&scope=' % LRD_API_KEY
LRD_LINKEDIN_AUTH_URL = 'https://lokerhub.hub.loginradius.com/requesthandlor.aspx?apikey=%s&provider=linkedin&callback=&scope=' % LRD_API_KEY