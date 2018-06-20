from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from project.modules import views

app_name = 'modules'
urlpatterns = [
    url(r'^$', views.ModulesView.as_view(), name='modules'),
    url(r'^my_modules/$', login_required(views.MyModulesView.as_view()), name='my_modules'),
    url(r'^(?P<pk>[0-9]+)/$', views.ModuleProgressView.as_view(), name='module'),
]
