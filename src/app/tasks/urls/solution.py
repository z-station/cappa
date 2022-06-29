from django.conf.urls import url
from app.tasks.views import (
    SolutionView,
    SolutionsView,
    SolutionsDiffView,
)


urlpatterns = [
    url(
        '^(?P<pk>[0-9]+)/diff/(?P<pair>[0-9]+)/$',
        SolutionsDiffView.as_view(),
        name='diff'
    ),
    url('^(?P<pk>[0-9]+)/$', SolutionView.as_view(), name='solution'),
    url('^$', SolutionsView.as_view(), name='solutions'),
]
