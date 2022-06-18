from rest_framework.routers import DefaultRouter
from app.training.api.views import (
    Python38ViewSet,
    GCC74ViewSet,
    PrologDViewSet,
    PostgresqlViewSet,
    PascalViewSet,
    PhpViewSet,
    CSharpViewSet,
    JavaViewSet,
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
task_router.register(
    'taskitem/postgresql',
    PostgresqlViewSet,
    basename='taskitem-postgresql'
)
task_router.register(
    'taskitem/pascal',
    PascalViewSet,
    basename='taskitem-pascal'
)
task_router.register(
    'taskitem/php',
    PhpViewSet,
    basename='taskitem-php'
)
task_router.register(
    'taskitem/csharp',
    CSharpViewSet,
    basename='taskitem-csharp'
)
task_router.register(
    'taskitem/java',
    JavaViewSet,
    basename='taskitem-java'
)
task_router.register('courses', CourseViewSet, basename='courses')

urlpatterns = task_router.urls
