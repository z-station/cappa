import os
import sys
from django.core.wsgi import get_wsgi_application
from app.settings import SENTRY_DSN

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")
sys.path[0:0] = [os.path.expanduser("~/django")]


if SENTRY_DSN:
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration

    sentry_sdk.init(
        dsn=SENTRY_DSN,
        traces_sample_rate=0.5,
        integrations=[DjangoIntegration()],
    )

application = get_wsgi_application()
