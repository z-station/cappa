# -*- coding: utf-8 -*-
import os

DEBUG = True
ALLOWED_HOSTS = ["*"]
# do not use this SECRET_KEY on production
SECRET_KEY = '!s0x%u7k9!9l+34ol54z_pofekso)39+iy__5r%bktb-n^56to'
LANGUAGE_CODE = 'ru-ru'
PYTHON_PATH = 'python3'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
SRC_DIR = os.path.join(PROJECT_ROOT, 'src')
TESTS_DIR = os.path.join(PROJECT_ROOT, 'tests')
MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media')
TMP_DIR = os.path.join(PROJECT_ROOT, "tmp")
PY_TMP_DIR = os.path.join(TMP_DIR, 'python')

access_mode = 0o744
os.makedirs(TMP_DIR, access_mode, exist_ok=True)
os.makedirs(PY_TMP_DIR, access_mode, exist_ok=True)
os.makedirs(MEDIA_ROOT, access_mode, exist_ok=True)

MEDIA_URL = '/media/'
STATIC_URL = '/static/'
ROOT_URLCONF = 'src.urls'
WSGI_APPLICATION = 'src.wsgi.application'

STATICFILES_DIRS = [
    os.path.join(SRC_DIR, 'static'),
]
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(SRC_DIR, 'templates'), ],
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
                'src.service.context_processors.site_settings'
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
    'src.profile',
    'tinymce',
    'mptt',
    'django_admin_listfilter_dropdown',
    'adminsortable2',
    'src',
    'src.news',
    'src.tasks',
    'src.training',
    'src.langs',
    'src.groups',
    'src.service'
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
        "HOST": "localhost",
        'PORT': '5432',
        "NAME": "cappa",
        "USER": "cappa",
        "PASSWORD": "cappa",
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
DEFAULT_FROM_EMAIL = 'info@cappa.ru'

AUTHENTICATION_BACKENDS = ['src.profile.backends.CustomModelBackend']

# ~========== ADMIN REORDER ===========~
INSTALLED_APPS += ['admin_reorder']
MIDDLEWARE += ['src.admin.middleware.CustomModelAdminReorder']
ADMIN_REORDER = (
    {
        'app': 'training', 'label': u'Учебные курсы',
        'models': ('training.Course', 'groups.Group', 'training.Solution', 'langs.Lang', )
    },
    {
        'app': 'tasks', 'label': u'Задачник',
        'models': ('tasks.Task', 'tasks.Tag', 'tasks.Source')
    },
    {
        'app': 'news', 'label': u'Контент',
        'models': ('news.News', 'service.Menu')
    },
)

# ~========== DOCKER SANDBOX ===========~
# Половину от всех ядер отдаем песочнице
cores_for_docker = ','.join([str(num) for num in range(os.cpu_count()//2)])
DOCKER_CONF = {
    "python": {
        "image_tag": "py-image",
        "container_name": "py-container",
        "path": os.path.join(SRC_DIR, 'langs', 'providers', 'python'),
        "dir": PY_TMP_DIR,
        "user": "sbox-user",
        "timeout_duration": 5,      # ограниечение на время выполнения скрипта в песочнице
        "cpuset_cpus": cores_for_docker,  # cpus - номера ядер, занимаемые конейнером
        'cpu_quota': -1,            # cpu-quota - максимум нагрузки на занимаемые ядра  (-1 это использование до 100%)
        "cpu_shares": 512,          # cpu-shares - относительное количество циклов процессора (относительно 1024)
        "mem_reservation": '256m',  # memory-reservation - мягкое ограничение на память
        "mem_limit": '512m',        # memory - жесткое ограничение на память
        "memswap_limit": '512m',    # memory-swap - Ограничение на файл подкачки
    }
}