from django.conf.urls import url, include

urlpatterns = [
    url(r'^translators/', include('app.translators.api.urls')),
    url(r'^training/', include('app.training.api.urls')),
    url(r'^groups/', include('app.groups.api.urls')),
    url(r'^tasks/', include('app.tasks.api.urls')),
]
