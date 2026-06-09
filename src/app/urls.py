from django.urls import path, include
from django.views.generic.base import TemplateView
from django.conf import settings
from django.views.static import serve
from django.contrib import admin
from filebrowser.sites import site

urlpatterns = [
    path('api/', include('app.api_urls')),
    path(
        'admin/filebrowser/',
        include((site.get_urls(), site.app_name), namespace=site.name)
    ),
    path('admin/', admin.site.urls),
    path(
        'media/<path:path>',
        serve,
        {'document_root': settings.MEDIA_ROOT}
    ),
    path(
        'static/<path:path>',
        serve,
        {'document_root': settings.STATIC_ROOT}
    ),
    path('courses/', include('app.training.urls', namespace='training')),
    path('solutions/', include('app.tasks.urls.solution', namespace='solutions')),
    path('groups/', include('app.groups.urls', namespace='groups')),
    path('taskbook/', include('app.taskbook.urls', namespace='taskbook')),
    path('tinymce/', include('tinymce.urls')),
    path('auth/', include('app.auth.urls', namespace='auth')),
    path('', TemplateView.as_view(template_name='frontpage.html')),
]

try:
    from app.service.models import SiteSettings
    admin.site.site_header = SiteSettings.objects.get(id=settings.SITE_ID).name
except Exception:
    pass
