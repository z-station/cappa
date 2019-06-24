from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic.base import TemplateView
from django.conf import settings
from django.views.static import serve

from project.profile.views import MyLoginView, MyLogoutView, MySignupView, MyEmailVerifySentView, MyEmailConfirmView, \
    MyPasswordResetView, MyPasswordResetFromKeyView, MyPasswordResetDoneView, PasswordResetFromKeyDoneView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    url(r'^courses/', include('project.courses.urls')),
    url(r'^executor/', include('project.executors.urls')),
    url(r'^groups/', include('project.groups.urls')),
    url(r'^modules/', include('project.modules.urls')),
    url(r'^tinymce/', include('tinymce.urls')),

    url(r'^login/$', MyLoginView.as_view(), name='account_login'),
    url(r'^logout/$', MyLogoutView.as_view(), {'next_page': '/'}, name='account_logout'),
    url(r'^register/$', MySignupView.as_view(), {'next_page': '/login/'}, name='account_signup'),
    url(r"^confirm-email/$", MyEmailVerifySentView.as_view(), name="account_email_verification_sent"),
    url(r"^confirm-email/(?P<key>[-:\w]+)/$", MyEmailConfirmView.as_view(), name="account_confirm_email"),
    url(r'^password/reset/$', MyPasswordResetView.as_view(), {'next_page': '/'}, name='account_reset_password'),
    url(r"^password/reset/done/$", MyPasswordResetDoneView.as_view(), name="account_reset_password_done"),
    url(r"^password/reset/key/(?P<uidb36>[0-9A-Za-z]+)-(?P<key>.+)/$", MyPasswordResetFromKeyView.as_view(),
        name="account_reset_password_from_key"),
    url(r"^password/reset/key/done/$", PasswordResetFromKeyDoneView.as_view(),
        name="account_reset_password_from_key_done"),
    url(r'^profile/', include('project.profile.urls')),

    url(r'^$', TemplateView.as_view(template_name='frontpage.html'))
]


