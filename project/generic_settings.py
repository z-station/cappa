# -*- coding: utf-8 -*-
import os

DEBUG = False
ALLOWED_HOSTS = ["*", ]

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media')
try:
    os.stat(MEDIA_ROOT)
except:
    os.mkdir(MEDIA_ROOT)

MEDIA_URL    = '/media/'
STATIC_URL   = '/static/'
ROOT_URLCONF = 'project.urls'
WSGI_APPLICATION = 'project.wsgi.application'

STATICFILES_DIRS = [
    os.path.join(PROJECT_ROOT, 'project', 'static'),
]
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(PROJECT_ROOT, 'project', 'templates'), ],
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
             ],
         }
    },
]

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
]

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sites',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'tinymce',
    'mptt',
    'project',
    'project.sources',
    'project.courses',
    'project.executors',
    'project.groups',
    'project.modules',
    'project.news'
)

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'project.middleware.LoginRequiredMiddleware',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': "project",
        'USER': "project",
        'PASSWORD': "project",
        'PORT': 5432,
    }
}

SESSION_COOKIE_AGE = 4 * 60 * 60
SESSION_SAVE_EVERY_REQUEST = True

# Настройки tinymce
TINYMCE_DEFAULT_CONFIG = {
    'plugins': 'spellchecker',
    'theme_advanced_buttons1': 'save,newdocument,|,justifyleft,justifycenter,justifyright,justifyfull,|, hr,bold,italic,underline,|, bullist,numlist,|,formatselect,removeformat,cut,copy,paste,pastetext,pasteword,|,fontselect,fontsizeselect,|,forecolor,backcolor,',
    'theme_advanced_buttons2' : 'removeformat, cut,copy,paste,pastetext,pasteword,|,outdent,indent,blockquote,|,undo,redo,|,styleprops,spellchecker',
    'theme_advanced_buttons3': 'sub,sup,|,charmap',
    'theme_advanced_buttons4': ' code, |,bold,italic,underline,strikethrough',
    'width': '100%',
    'height': 300,
    'theme_advanced_resizing': 'True',
    'extended_valid_elements ': '*[*]',
}


SITE_ID = 1
# EMAIL_HOST = 'smtp.yandex.ru'
# EMAIL_PORT = 465
# EMAIL_HOST_USER = 'mailUser'
# EMAIL_HOST_PASSWORD = 'pass'
# EMAIL_USE_SSL = True
DEFAULT_FROM_EMAIL = 'info@cappa.ru'

# allauth
ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
ACCOUNT_EMAIL_REQUIRED = True
# --- Executors config
CODE_TMP_DIR = os.path.join(PROJECT_ROOT, "tmp")
try:
    os.stat(CODE_TMP_DIR)
except:
    os.mkdir(CODE_TMP_DIR)

# Настройки профиля
LOGIN_REDIRECT_URL = "/"
