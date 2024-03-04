from django.conf.urls import url, include
from django.views.generic.base import TemplateView
from django.conf import settings
from django.views.static import serve
from django.contrib import admin
from filebrowser.sites import site


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^admin/filebrowser/', include(site.urls)),
    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    url(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
    url(r'^pages/', include('app.training.urls', namespace='training')),
    url(r'^tinymce/', include('tinymce.urls')),
    url(r'^auth/', include('app.auth.urls', namespace='auth')),
    url(r'^$', TemplateView.as_view(template_name='frontpage.html'))
]

try:
    from app.service.models import SiteSettings
    admin.site.site_header = SiteSettings.objects.get(id=settings.SITE_ID).name
except:
    pass
