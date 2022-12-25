from django.conf.urls import url, include

urlpatterns = [
    url(
        regex=r'^translators/',
        view=include('app.translators.api.urls')
    ),
    url(
        regex=r'^training/',
        view=include('app.training.api.urls')
    ),
    url(
        regex=r'^groups/',
        view=include('app.groups.api.urls')
    ),
    url(
        regex=r'^tasks/',
        view=include('app.tasks.api.urls')
    ),
]
