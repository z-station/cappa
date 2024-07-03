# -*- coding: utf-8 -*-
import os
from os import environ as env
from app.translators.enums import TranslatorType


if env.get('APP_DEBUG', None) is None:
    DEBUG = True
else:
    DEBUG = bool(env.get('APP_DEBUG') == 'debug')

ALLOWED_HOSTS = env.get('APP_ALLOWED_HOSTS', '*').split(',')

DEFAULT_SECRET_KEY = '!s0x%u7k9!9l+34ol54z_pofekso)39+iy__5r%bktb-n^56to'
SECRET_KEY = env.get('APP_SECRET_KEY', DEFAULT_SECRET_KEY)

LANGUAGE_CODE = 'ru-ru'

LANGUAGES = [
    ('ru', 'Русский'),
    ('en', 'Английский')
]
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
PROJECT_DIR = os.path.join(BASE_DIR, 'src', 'app')

DEFAULT_MEDIA_ROOT = os.path.join(BASE_DIR, 'public', 'media')
MEDIA_ROOT = env.get('APP_MEDIA_ROOT', DEFAULT_MEDIA_ROOT)
try:
    os.makedirs(MEDIA_ROOT, mode=0o766, exist_ok=True)
except PermissionError:
    pass

DEFAULT_STATIC_ROOT = os.path.join(BASE_DIR, 'public', 'static')
STATIC_ROOT = env.get('APP_STATIC_ROOT', DEFAULT_STATIC_ROOT)

SQL_FILES_DIR = os.path.join(BASE_DIR, 'public', 'sql_files')

MEDIA_URL = '/media/'
STATIC_URL = '/static/'
LOGIN_URL = '/auth/signin/'
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
    'filebrowser',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sites',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework.authtoken',
    'django_filters',
    'tinymce',
    'mptt',
    'django_admin_listfilter_dropdown',
    'adminsortable2',
    'app',
    'app.accounts',
    'app.news',
    'app.tasks',
    'app.databases',
    'app.training',
    'app.groups',
    'app.service',
    'app.taskbook',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'app.auth.middleware.LastSeenUserMiddleware'
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
# Хранить в кэше вечно дату последнего онлайна пользователя
LAST_SEEN_CACHE_TIMEOUT = None
# Пользователь считается онлайн если посылает запросы
# не реже чем раз в 300 сек (5 мин)
USER_ONLINE_TIMEOUT = 300

SESSION_COOKIE_AGE = 4 * 60 * 60
SESSION_SAVE_EVERY_REQUEST = True

# Настройки tinymce
TINYMCE_DEFAULT_CONFIG = {
    'plugins': 'table, spellchecker, advlink, contextmenu, advimage, inlinepopups, preview, media',
    'theme_advanced_buttons1':
        'spellchecker, undo,redo,|,'
        'bold,italic,underline,strikethrough,|,'
        'justifyleft,justifycenter,justifyright,justifyfull,|,'
        'bullist,numlist,blockquote,|,'
        'formatselect,|,'
        'fontsizeselect,|,'
        'forecolor,backcolor,table,|,'
        'removeformat,|,code, |,'
        'link,unlink, image, |,',
    'width': '100%',
    'height': 100,
    'theme_advanced_resizing': 'True',
    'extended_valid_elements ': '*[*]',
    'content_style': '.mcecontentbody{font-size:14px;}',
    'external_image_list_url': 'images/',
    'external_link_list_url': 'links/',
    'paste_remove_styles': 'true',
    'paste_remove_styles_if_webkit': 'true',
    'paste_strip_class_attributes': 'all',
}
TINYMCE_SPELLCHECKER = True


SITE_ID = 1
DEFAULT_FROM_EMAIL = env.get('APP_EMAIL', 'info@app.ru')

AUTH_USER_MODEL = 'accounts.User'
AUTHENTICATION_BACKENDS = ['app.auth.backends.CustomModelBackend']

DATA_UPLOAD_MAX_MEMORY_SIZE = 52428800 # 50Mb

# ~========== ADMIN REORDER ===========~
INSTALLED_APPS += ['admin_reorder']
MIDDLEWARE += ['app.admin.middleware.CustomModelAdminReorder']
ADMIN_REORDER = (
    {
        'app': 'training', 'label': u'Учебные курсы',
        'models': ('training.Course', 'groups.Group')
    },
    {
        'app': 'filebrowser',  'label': u'Менеджер файлов',
    },
    {
        'app': 'tasks', 'label': u'Архив задач',
        'models': (
            'tasks.Task',
            'tasks.Tag',
            'tasks.Solution',
            'tasks.ExternalSolution',
            'tasks.Source',
            'tasks.Checker',
        )
    },
    {
        'app': 'taskbook', 'label': u'Задачник',
        'models': ('taskbook.TaskBookItem',)
    },
    {
        'app': 'databases', 'label': u'Пользовательские базы данных',
        'models': ('databases.Database',)
    },
    {
        'app': 'news', 'label': u'Контент',
        'models': ('news.News', 'service.Menu')
    }
)

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
    ]
}

SERVICES_HOSTS = {
    TranslatorType.PYTHON38: env.get(
        'PYTHON38_HOST', 'http://localhost:9001'
    ),
    TranslatorType.GCC74: env.get(
        'GCC74_HOST', 'http://localhost:9002'
    ),
    TranslatorType.PROLOG_D: env.get(
        'PROLOGD_HOST', 'http://localhost:9003'
    ),
    TranslatorType.POSTGRESQL: env.get(
        'POSTGRESQL_HOST', 'http://localhost:9004'
    ),
    TranslatorType.PASCAL: env.get(
        'PASCAL_HOST', 'http://localhost:9005'
    ),
    TranslatorType.PHP: env.get(
        'PHP_HOST', 'http://localhost:9006'
    ),
    TranslatorType.CSHARP: env.get(
        'CSHARP_HOST', 'http://localhost:9007'
    ),
    TranslatorType.JAVA: env.get(
        'JAVA_HOST', 'http://localhost:9008'
    ),
}

ANTIPLAG_HOST = env.get(
    'ANTIPLAG_HOST', 'http://localhost:9020'
)

# ~========== FILEBROWSER ===========~

FILEBROWSER_DIRECTORY = "filebrowser/"

FILEBROWSER_EXTENSIONS = {
    'Image': ['.jpg', '.jpeg', '.gif', '.png', '.tif', '.tiff', '.webp'],
    'Document': ['Any extensions'],
    'Video': ['.mov', '.mp4', '.mkv'],
    'Audio': ['.mp3',]
}

FILEBROWSER_VERSIONS = {
    'thumbnail': {
        'verbose_name': 'Thumbnail',
        'width': 100,
        'height': 100,
        'opts': 'crop'
    },
}

FILEBROWSER_VERSION_QUALITY = 90
FILEBROWSER_ADMIN_VERSIONS = ['thumbnail']
FILEBROWSER_ADMIN_THUMBNAIL = 'thumbnail'
FILEBROWSER_MAX_UPLOAD_SIZE = 500*1048576   # 500 mb
FILEBROWSER_NORMALIZE_FILENAME = True
FILEBROWSER_CONVERT_FILENAME = True
FILEBROWSER_LIST_PER_PAGE = 20
FILEBROWSER_DEFAULT_SORTING_BY = "date"
FILEBROWSER_DEFAULT_SORTING_ORDER = "desc"
FILEBROWSER_SEARCH_TRAVERSE = True
FILEBROWSER_OVERWRITE_EXISTING = False
