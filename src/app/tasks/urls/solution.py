from django.conf.urls import url
from app.tasks.views import (
    SolutionView,
    SolutionsView,
    SolutionsDiffView,
)


urlpatterns = [
    url(
        regex='^(?P<pk>[0-9]+)/diff/(?P<pair>[0-9]+)/$',
        view=SolutionsDiffView.as_view(),
        name='diff'
    ),
    url(
        regex='^(?P<pk>[0-9]+)/$',
        view=SolutionView.as_view(),
        name='solution'
    ),
    url(
        regex='^$',
        view=SolutionsView.as_view(),
        name='solutions'
    ),
]
