from rest_framework.routers import DefaultRouter
from app.training.api.views import (
    PrologDViewSet,
    Python38ViewSet,
    GCC74ViewSet,
    CourseViewSet
)

task_router = DefaultRouter()
task_router.register(
    'taskitem/python38',
    Python38ViewSet,
    basename='taskitem-python38'
)
task_router.register(
    'taskitem/gcc74',
    GCC74ViewSet,
    basename='taskitem-gcc74'
)
task_router.register(
    'taskitem/prolog-d',
    PrologDViewSet,
    basename='taskitem-prolog-d'
)
task_router.register('courses', CourseViewSet, basename='courses')

urlpatterns = task_router.urls
