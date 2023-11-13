from django.conf.urls import url
from app.training import views

urlpatterns = [
    url('^$', views.CourseListView.as_view(), name='courses'),
    url('^(?P<course>[a-z0-9-]+)/$', views.CourseView.as_view(), name='course'),
    url('^(?P<course>[a-z0-9-]+)/(?P<topic>[a-z0-9-]+)/$', views.TopicView.as_view(), name='topic'),
]
