# -*- coding: utf-8 -*-
import os
from os import environ as env

DEBUG = env.get('APP_DEBUG', True)

ALLOWED_HOSTS = env.get('APP_ALLOWED_HOSTS', '*').split(',')

DEFAULT_SECRET_KEY = '!s0x%u7k9!9l+34ol54z_pofekso)39+iy__5r%bktb-n^56to'
SECRET_KEY = env.get('APP_SECRET_KEY', DEFAULT_SECRET_KEY)

LANGUAGE_CODE = 'ru-ru'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
PROJECT_DIR = os.path.join(BASE_DIR, 'src', 'app')

DEFAULT_MEDIA_ROOT = os.path.join(BASE_DIR, 'public', 'media')
MEDIA_ROOT = env.get('APP_MEDIA_ROOT', DEFAULT_MEDIA_ROOT)
try:
    os.makedirs(MEDIA_ROOT, mode=0o766, exist_ok=True)
except PermissionError:
    pass

DEFAULT_STATIC_ROOT = os.path.join(BASE_DIR, 'public', 'static')
STATIC_ROOT = env.get('APP_STATIC_ROOT', DEFAULT_STATIC_ROOT)

MEDIA_URL = '/media/'
STATIC_URL = '/static/'
ROOT_URLCONF = 'app.urls'
WSGI_APPLICATION = 'app.wsgi.application'

STATICFILES_DIRS = [
    os.path.join(PROJECT_DIR, 'static'),
]
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(PROJECT_DIR, 'templates'), ],
        'APP_DIRS': False,
        'OPTIONS': {
            'debug': DEBUG,
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
                'django.template.loaders.eggs.Loader',
            ],
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'app.service.context_processors.site_settings'
             ],
         }
    },
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sites',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app.profile',
    'tinymce',
    'mptt',
    'django_admin_listfilter_dropdown',
    'adminsortable2',
    'app',
    'app.news',
    'app.tasks',
    'app.training',
    'app.groups',
    'app.service'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        'NAME': env.get('POSTGRES_DB', 'cappa'),
        'USER': env.get('POSTGRES_USER', 'cappa'),
        'PASSWORD': env.get('PGPASSWORD', 'cappa'),
        'HOST': env.get('POSTGRES_HOST', 'localhost'),
        'PORT': env.get('POSTGRES_PORT', 5432)
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

SESSION_COOKIE_AGE = 4 * 60 * 60
SESSION_SAVE_EVERY_REQUEST = True

# Настройки tinymce
TINYMCE_DEFAULT_CONFIG = {
    'plugins': 'spellchecker',
    'theme_advanced_buttons1':
        'undo,redo,|,bold,italic,underline,strikethrough,|,justifyleft,justifycenter,justifyright,justifyfull,|,'
        'bullist,numlist,blockquote,|,formatselect,|,fontsizeselect,|,forecolor,backcolor,|,'
        'removeformat,|,code',
    'width': '100%',
    'height': 100,
    'theme_advanced_resizing': 'True',
    'extended_valid_elements ': '*[*]',
    'content_style': '.mcecontentbody{font-size:14px;}',
}


SITE_ID = 1
DEFAULT_FROM_EMAIL = env.get('APP_EMAIL', 'info@app.ru')

AUTHENTICATION_BACKENDS = ['app.profile.backends.CustomModelBackend']

# ~========== ADMIN REORDER ===========~
INSTALLED_APPS += ['admin_reorder']
MIDDLEWARE += ['app.admin.middleware.CustomModelAdminReorder']
ADMIN_REORDER = (
    {
        'app': 'training', 'label': u'Учебные курсы',
        'models': ('training.Course', 'groups.Group', 'training.Solution')
    },
    {
        'app': 'tasks', 'label': u'Задачник',
        'models': ('tasks.Task', 'tasks.Tag', 'tasks.Source')
    },
    {
        'app': 'news', 'label': u'Контент',
        'models': ('news.News', 'service.Menu')
    }
)

# ~========== TRANSLATORS HOSTS ===========~
SERVICES = {
    "PYTHON38": {
        "EXTERNAL_URL": env.get('PYTHON38_EXTERNAL_URL', 'http://localhost:9001'),
        "INTERNAL_URL": env.get('PYTHON38_INTERNAL_URL', 'http://localhost:9001')
    },
    "GCC74": {
        "EXTERNAL_URL": env.get('GCC74_EXTERNAL_URL', 'http://localhost:9002'),
        "INTERNAL_URL": env.get('GCC74_INTERNAL_URL', 'http://localhost:9002')
    }
}
