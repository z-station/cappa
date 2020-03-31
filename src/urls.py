from django.conf.urls import url, include
from django.views.generic.base import TemplateView
from django.conf import settings
from django.views.static import serve
from django.contrib import admin


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    url(r'^courses/', include('src.training.urls', namespace='training')),
    url(r'^groups/', include('src.groups.urls', namespace='groups')),
    url(r'^tinymce/', include('tinymce.urls')),
    url(r'^', include('src.profile.urls', namespace='profile')),
    url(r'^$', TemplateView.as_view(template_name='frontpage.html'))
]

# if settings.DEBUG:
#     import debug_toolbar
#     urlpatterns = [
#         url('__debug__/', include(debug_toolbar.urls)),
#     ] + urlpatterns
#

try:
    from src.service.models import SiteSettings
    admin.site.site_header = SiteSettings.objects.get(id=settings.SITE_ID).name
except:
    pass
