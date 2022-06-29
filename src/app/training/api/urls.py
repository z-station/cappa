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
    CourseViewSet,
    TaskItemViewSet,
)

router = DefaultRouter()
router.register(
    'taskitem/python38',
    Python38ViewSet,
    basename='taskitem-python38'
)
router.register(
    'taskitem/gcc74',
    GCC74ViewSet,
    basename='taskitem-gcc74'
)
router.register(
    'taskitem/prolog-d',
    PrologDViewSet,
    basename='taskitem-prolog-d'
)
router.register(
    'taskitem/postgresql',
    PostgresqlViewSet,
    basename='taskitem-postgresql'
)
router.register(
    'taskitem/pascal',
    PascalViewSet,
    basename='taskitem-pascal'
)
router.register(
    'taskitem/php',
    PhpViewSet,
    basename='taskitem-php'
)
router.register(
    'taskitem/csharp',
    CSharpViewSet,
    basename='taskitem-csharp'
)
router.register(
    'taskitem/java',
    JavaViewSet,
    basename='taskitem-java'
)
router.register('courses', CourseViewSet, basename='courses')
router.register('taskitem', TaskItemViewSet, basename='taskitem')

urlpatterns = router.urls
