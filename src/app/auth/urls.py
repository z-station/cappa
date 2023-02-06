from django.conf.urls import url
from . import views


urlpatterns = [
    url(
        regex='^signin/$',
        view=views.SignInView.as_view(),
        name='signin'
    ),
    url(
        regex='^signout/$',
        view=views.SignOutView.as_view(),
        name='signout'
    ),
    url(
        regex='^signup/$',
        view=views.SignUpView.as_view(),
        name='signup'
    ),
]
