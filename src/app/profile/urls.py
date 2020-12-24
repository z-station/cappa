from django.conf.urls import url
from . import views


urlpatterns = [
    url('^login/$', views.LoginView.as_view(), name='login'),
    url('^logout/$', views.logout, name='logout'),
    url('^signup/$', views.SignUpView.as_view(), name='signup'),
]