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

# STATIC_ROOT  = os.path.join(PROJECT_ROOT, 'project/static')

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
]

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'tinymce',
    'project.courses',
    'project.executors',
    'project.groups',
    'project.modules',
    'admin_reorder',
)

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'admin_reorder.middleware.ModelAdminReorder',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(PROJECT_ROOT, 'project.sqlite3'),
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
# Настройки admin_reorder
ADMIN_REORDER = (
    {'app': "auth", 'label': "Администрирование", 'models': ('auth.User', 'auth.Group', )},
    {'app': 'courses', "label": "Курсы", 'models': ('сourses.TreeItem', 'сourses.TreeItemFlat', )},
    {'app': 'executors', "label": "Коды и решения", 'models': ('executors.CodeFlat', 'executors.CodeSolution',)},
    {'app': 'modules', "label": "Модули и группы", 'models': ('modules.Module', 'groups.Group', )}
)

# --- Executors config

CODE_TMP_DIR = os.path.join(PROJECT_ROOT, "tmp")
try:
    os.stat(CODE_TMP_DIR)
except:
    os.mkdir(CODE_TMP_DIR)
