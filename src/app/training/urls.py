from django.urls import path
from app.training import views

app_name = 'training'

urlpatterns = [
    path('', views.CourseListView.as_view(), name='courses'),
    path('<slug:course>/', views.CourseView.as_view(), name='course'),
    path('<slug:course>/<slug:topic>/', views.TopicView.as_view(), name='topic'),
    path(
        '<slug:course>/<slug:topic>/<slug:taskitem>/',
        views.TaskItemView.as_view(),
        name='taskitem'
    ),
]
