import os
import sys
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")
sys.path[0:0] = [os.path.expanduser("~/django")]

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

