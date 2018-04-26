from django.conf.urls import url
from project.executors.views import execute

urlpatterns = [
    url("^execute/", execute, name='execute'),
]