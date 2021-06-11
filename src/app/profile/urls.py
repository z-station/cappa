from django.conf.urls import url
from . import views


urlpatterns = [
    url('^signin/$', views.SignInView.as_view(), name='signin'),
    url('^signout/$', views.SignOutView.as_view(), name='signout'),
    url('^signup/$', views.SignUpView.as_view(), name='signup'),
]