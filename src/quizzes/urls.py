from django.conf.urls import url
from . import views

urlpatterns = [
    url('^$', views.QuizListView.as_view(), name='quizzes'),
    url('^(?P<quiz>[a-z0-9-]+)/$', views.QuizView.as_view(), name='quiz'),
    url('^(?P<quiz>[a-z0-9-]+)/solutions/$', views.QuizSolutionsView.as_view(), name='quiz-solutions'),
#    url('^(?P<quiz>[a-z0-9-]+)/$', views.TopicView.as_view(), name='topic'),
    url('^(?P<quiz>[a-z0-9-]+)/(?P<taskitem>[a-z0-9-]+)/$', views.TaskItemView.as_view(), name='taskitem'),
    url('^(?P<quiz>[a-z0-9-]+)/(?P<taskitem>[a-z0-9-]+)/solution/$', views.SolutionView.as_view(), name='solution'),
]
