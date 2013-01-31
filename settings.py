# Django settings for gamehelper project.

DEBUG = True
TEMPLATE_DEBUG = True

ADMINS = (
  ('Nikolay Amiantov', 'nikoamia@gmail.com'),
)

MANAGERS = ADMINS

import os.path

DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
    'NAME': os.path.join(os.path.dirname(__file__), 'database.db').replace('\\','/'), # Or path to database file if using sqlite3.
    'USER': '',            # Not used with sqlite3.
    'PASSWORD': '',        # Not used with sqlite3.
    'HOST': '',            # Set to empty string for localhost. Not used with sqlite3.
    'PORT': '',            # Set to empty string for default. Not used with sqlite3.
  }
}

# Make this unique, and don't share it with anybody.
# TODO: change for production
SECRET_KEY = '0aivt0o7%i@&z0e9dfoftrk2ys7nyymvzdpck+)5tc(kw!%!m^'

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# TODO: Until Django 1.5
from django.core.urlresolvers import reverse_lazy
LOGIN_URL = reverse_lazy('login')
LOGIN_REDIRECT_URL = reverse_lazy('root')

CACHE_MIDDLEWARE_ALIAS = 'default'

CACHE_MIDDLEWARE_SECONDS = 0

CACHE_MIDDLEWARE_KEY_PREFIX = 'gamehelper'

import os.path

# Additional locations of static files
STATICFILES_DIRS = (
  # Put strings here, like "/home/html/static" or "C:/www/django/static".
  # Always use forward slashes, even on Windows.
  # Don't forget to use absolute paths, not relative paths.
  os.path.join(os.path.dirname(__file__), 'static').replace('\\','/'),
)

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Moscow'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'ru-RU'

SITE_ID = 1

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
  'django.contrib.staticfiles.finders.FileSystemFinder',
  'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#  'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
  'django.template.loaders.filesystem.Loader',
  'django.template.loaders.app_directories.Loader',
#  'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
  'django.middleware.cache.UpdateCacheMiddleware',
  'django.middleware.common.CommonMiddleware',
  'django.middleware.transaction.TransactionMiddleware',
  'django.contrib.sessions.middleware.SessionMiddleware',
  'django.middleware.csrf.CsrfViewMiddleware',
  'django.contrib.auth.middleware.AuthenticationMiddleware',
  'django.middleware.locale.LocaleMiddleware',
  'django.contrib.messages.middleware.MessageMiddleware',
  'misc.middleware.Http403Middleware',
  'django.middleware.cache.FetchFromCacheMiddleware',
  # Uncomment the next line for simple clickjacking protection:
  # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'urls'

import os.path

TEMPLATE_DIRS = (
  # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
  # Always use forward slashes, even on Windows.
  # Don't forget to use absolute paths, not relative paths.
  os.path.join(os.path.dirname(__file__), 'templates').replace('\\','/'),
)

INSTALLED_APPS = (
  'django.contrib.auth',
  'django.contrib.contenttypes',
  'django.contrib.sessions',
  'django.contrib.sites',
  'django.contrib.messages',
  'django.contrib.staticfiles',
  # Uncomment the next line to enable the admin:
  'django.contrib.admin',
  # Uncomment the next line to enable admin documentation:
  'django.contrib.admindocs',
  'django.contrib.comments',
  'users_ex',
  'messages',
  'games',
  'generic_game',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
  'version': 1,
  'disable_existing_loggers': True,
  'formatters': {
    'simple': {
      'format': '%(levelname)s %(module)s %(message)s'
    }
  },
  'filters': {
    'require_debug_false': {
      '()': 'django.utils.log.CallbackFilter',
      'callback': lambda r: not DEBUG
    }
  },
  'handlers': {
    'console':{
      'level': 'DEBUG',
      'class': 'logging.StreamHandler',
      'formatter': 'simple',
    },
  },
  'loggers': {
    'django': {
      'level': 'WARNING',
      'handlers': ['console'],
      'propagate': True,
    },
    'default': {
      'level': 'DEBUG',
      'handlers': ['console'],
      'propagate': True,
    },
  }
}

APPEND_SLASH = True

CACHES = {
  'default': {
    'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
  },
   'database': {
    'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
    'LOCATION': 'cache',
  }
}

GAME_TYPE_CLASSES = (
  'generic_game.game_types.GenericGameType',
)

ADD_USERS_TO_DEFAULT_GROUP = True

DEFAULT_GROUP_NAME = "Default"
