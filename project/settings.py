from .generic_settings import *

DEBUG = True
TEMPALTE_DEBUG = DEBUG

EMAIL_PORT = 1025
EMAIL_HOST = 'localhost'

SECRET_KEY = 'behv8h(w06x^zv)h(ecfuij0g(3&@)h&xid_s(gxoslx^=ls=_'

# INSTALLED_APPS += (
#     'debug_toolbar',
# )
#
# MIDDLEWARE_CLASSES += (
#     'debug_toolbar.middleware.DebugToolbarMiddleware',
# )

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

# from django.core.cache import cache
# cache.clear()