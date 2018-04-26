from django.conf.urls import url, include
from django.contrib import admin
from project.views import frontpage

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^cms/',  include('project.cms.urls')),
    url(r'^tinymce/', include('tinymce.urls')),
    url(r'^executor/', include('project.executors.urls')),
    url(r'^groups/', include('project.groups.urls')),
    url(r'^modules/', include('project.modules.urls')),
    url(r'^$', frontpage),
]
