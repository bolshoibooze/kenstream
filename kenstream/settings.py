from __future__ import absolute_import

import logging
import os.path
import datetime
from datetime import timedelta

logger = logging.getLogger()

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PROJECT_DIR  = os.path.dirname(__file__)


SECRET_KEY = '*+1=!%9whi-((4_e)b2w-4=90-2b!_dd_h_=coxg)%7-mg^tw7'

DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['*']


SITE_ID = 1


INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'yawdadmin',
    'django.contrib.admin',
    'django.contrib.admindocs',
    #'django.contrib.markup',
    'django.contrib.sitemaps',
    'django.contrib.formtools',
    'fluent_comments',
    'crispy_forms',
    'django_comments',
    #'django.contrib.comments',
    
    'accounts',
    'watchlist',
    'ua_detector',
    'likes',
    
    #other apps 
    'sorl.thumbnail',
    'admin_honeypot',
    'secretballot',
    'form_utils',
    'tinymce',
    'avatar',
)

AUTH_USER_MODEL = 'accounts.CustomUser'

FLUENT_COMMENTS_EXCLUDE_FIELDS = ('name', 'email', 'url',)
COMMENTS_APP = 'fluent_comments'

AUTHENTICATION_BACKENDS = (
    
    'django.contrib.auth.backends.ModelBackend',
)


#see: https://github.com/pozytywnie/django-facebook-auth

MIDDLEWARE_CLASSES = (
    'django.middleware.cache.UpdateCacheMiddleware',
    #'htmlmin.middleware.HtmlMinifyMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
    #'htmlmin.middleware.MarkRequestMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',

    'django.middleware.csrf.CsrfViewMiddleware',
    #'django.core.context_processors.csrf',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.RemoteUserMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'yawdadmin.middleware.PopupMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
    'secretballot.middleware.SecretBallotIpUseragentMiddleware',
    'likes.middleware.SecretBallotUserIpUseragentMiddleware',
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)



TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',    
    'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.request',
)


TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)

#HTML_MINIFY = True

ROOT_URLCONF = 'kenstream.urls'

WSGI_APPLICATION = 'kenstream.wsgi.application'



DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Africa/Nairobi'

USE_I18N = True

USE_L10N = True

USE_TZ = True



MEDIA_ROOT = os.path.join(PROJECT_DIR, 'static/media/')

MEDIA_URL = '/static/media/'

STATIC_ROOT = ''

STATIC_URL = '/static/'

STATICFILES_DIRS = (
   os.path.join(os.path.dirname(__file__), 'static'),
    
)




GENDER = (
   ('Male','Male'),
   ('Female','Female')
)


TYPE = (
   ('Movie','Movie'),
   ('Series','Series'),
   ('T.V Show','T.V Show'),
   ('Feature Film','Feature Film'),
   ('Documentary','Documentary')
)

RATINGS = (
   ('Must-watch','Must-watch'),
   ('Good stuff','Good stuff'),
   ('Average','Average'),
   ('Pathetic','Pathetic')
)


