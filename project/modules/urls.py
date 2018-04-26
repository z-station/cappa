from django.conf.urls import url

from . import views

app_name = 'modules'
urlpatterns = [
    url(r'^$', views.ModulesView.as_view(), name='modules'),
    url(r'^(?P<pk>[0-9]+)/$', views.ModuleView.as_view(), name='module'),
]
