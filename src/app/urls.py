from django.conf.urls import url, include
from django.views.generic.base import TemplateView
from django.conf import settings
from django.views.static import serve
from django.contrib import admin

urlpatterns = [
    url(r'^api/', include('app.api_urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    url(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
    url(r'^courses/', include('app.training.urls', namespace='training')),
    url(r'^solutions/', include('app.tasks.urls.solution', namespace='solutions')),
    url(r'^groups/', include('app.groups.urls', namespace='groups')),
    url(r'^tinymce/', include('tinymce.urls')),
    url(r'^auth/', include('app.auth.urls', namespace='auth')),
    url(r'^$', TemplateView.as_view(template_name='frontpage.html'))
]

try:
    from app.service.models import SiteSettings
    admin.site.site_header = SiteSettings.objects.get(id=settings.SITE_ID).name
except:
    pass
