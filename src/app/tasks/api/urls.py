from rest_framework.routers import DefaultRouter
from app.tasks.api.views.task import (
    TaskViewSet
)

task_router = DefaultRouter()
task_router.register('', TaskViewSet, basename='tasks')

urlpatterns = task_router.urls
