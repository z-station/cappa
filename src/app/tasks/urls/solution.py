from django.conf.urls import url
from app.tasks.views import (
    SolutionView,
    SolutionsView,
)


urlpatterns = [
    url('^(?P<pk>[0-9]+)/$', SolutionView.as_view(), name='solution'),
    url('^$', SolutionsView.as_view(), name='solutions'),
]
