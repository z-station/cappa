from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from . import views

app_name = 'modules'
urlpatterns = [
    url(r'^$', views.ModulesView.as_view(), name='modules'),
    url(r'^my_modules/$', login_required(views.MyModulesView.as_view()), name='my_modules'),
    url(r'^(?P<pk>[0-9]+)/$', views.ModuleView.as_view(), name='module'),
]
