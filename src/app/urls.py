from django.conf.urls import url, include
from django.views.generic.base import TemplateView
from django.conf import settings
from django.views.static import serve
from django.contrib import admin
from filebrowser.sites import site

urlpatterns = [
    url(
        regex=r'^api/',
        view=include('app.api_urls')
    ),
    url(
        regex=r'^admin/filebrowser/',
        view=include(site.urls)
    ),
    url(
        regex=r'^admin/',
        view=admin.site.urls
    ),
    url(
        regex=r'^media/(?P<path>.*)$',
        view=serve,
        kwargs={'document_root': settings.MEDIA_ROOT}
    ),
    url(
        regex=r'^static/(?P<path>.*)$',
        view=serve,
        kwargs={'document_root': settings.STATIC_ROOT}
    ),
    url(
        regex=r'^courses/',
        view=include('app.training.urls', namespace='training')
    ),
    url(
        regex=r'^solutions/',
        view=include('app.tasks.urls.solution', namespace='solutions')
    ),
    url(
        regex=r'^groups/',
        view=include('app.groups.urls', namespace='groups')
    ),
    url(
        regex=r'^taskbook/',
        view=include('app.taskbook.urls', namespace='taskbook')
    ),
    url(
        regex=r'^tinymce/',
        view=include('tinymce.urls')
    ),
    url(
        regex=r'^auth/',
        view=include('app.auth.urls', namespace='auth')
    ),
    url(
        regex=r'^$',
        view=TemplateView.as_view(template_name='frontpage.html')
    )
]

try:
    from app.service.models import SiteSettings
    admin.site.site_header = SiteSettings.objects.get(id=settings.SITE_ID).name
except:
    pass
