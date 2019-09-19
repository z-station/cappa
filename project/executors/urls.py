from django.conf.urls import url
from project.executors.views import execute, check_tests, user_solution, save_version

urlpatterns = [
    url("^execute/$", execute, name='execute'),
    url("^check_tests/$", check_tests, name='check_tests'),
    url("^save_version/$", save_version, name='save_version'),
    url("^solution-(?P<user_id>\d+)-(?P<code_id>\d+)/$", user_solution, name="user_solution"),
]