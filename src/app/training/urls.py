from django.conf.urls import url
from app.training import views

urlpatterns = [
    url(
        regex='^$',
        view=views.CourseListView.as_view(),
        name='courses'
    ),
    url(
        regex='^(?P<course>[-\w]+)/$',
        view=views.CourseView.as_view(),
        name='course'
    ),
    url(
        regex='^(?P<course>[-\w]+)/(?P<topic>[-\w]+)/$',
        view=views.TopicView.as_view(),
        name='topic'
    ),
    url(
        regex='^(?P<course>[-\w]+)/(?P<topic>[-\w]+)/(?P<taskitem>[-\w]+)/$',
        view=views.TaskItemView.as_view(),
        name='taskitem'
    ),
]
