from django.conf.urls import url
from project.executors.views import execute, check_tests

urlpatterns = [
    url("^execute/$", execute, name='execute'),
    url("^check_tests/$", check_tests, name='check_tests'),
]