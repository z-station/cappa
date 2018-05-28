from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.views.generic.base import TemplateView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^courses/',  include('project.courses.urls')),
    url(r'^executor/', include('project.executors.urls')),
    url(r'^groups/', include('project.groups.urls')),
    url(r'^modules/', include('project.modules.urls')),
    url(r'^tinymce/', include('tinymce.urls')),
    url(r'^login/$', auth_views.login, {'template_name': 'admin/login.html', }, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
    url(r'^$', TemplateView.as_view(template_name='frontpage.html'))
]
