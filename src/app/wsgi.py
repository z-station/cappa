import os
import sys
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")
sys.path[0:0] = [os.path.expanduser("~/django")]

# Импорт библиотеки Sentry SDK
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

# Импорт DSN из файла настроек
from app.settings import SENTRY_DSN

# Инициализация Sentry SDK
sentry_sdk.init(
    dsn=SENTRY_DSN,
    traces_sample_rate=1.0,
    #profiles_sample_rate=1.0,
    integrations=[DjangoIntegration()],
)

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

