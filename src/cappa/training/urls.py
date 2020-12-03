from django.conf.urls import url
from . import views

urlpatterns = [
    url('^$', views.CourseListView.as_view(), name='courses'),
    url('^(?P<course>[a-z0-9-]+)/$', views.CourseView.as_view(), name='course'),
    url('^(?P<course>[a-z0-9-]+)/solutions/$', views.CourseSolutionsView.as_view(), name='course-solutions'),
    url('^(?P<course>[a-z0-9-]+)/(?P<topic>[a-z0-9-]+)/$', views.TopicView.as_view(), name='topic'),
    url('^(?P<course>[a-z0-9-]+)/(?P<topic>[a-z0-9-]+)/(?P<taskitem>[a-z0-9-]+)/$', views.TaskItemView.as_view(), name='taskitem'),
    url('^(?P<course>[a-z0-9-]+)/(?P<topic>[a-z0-9-]+)/(?P<taskitem>[a-z0-9-]+)/solution/$', views.SolutionView.as_view(), name='solution'),
]
