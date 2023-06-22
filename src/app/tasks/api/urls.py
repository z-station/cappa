from rest_framework.routers import DefaultRouter
from app.tasks.api import views


router = DefaultRouter()

router.register(
    '',
    views.TaskViewSet,
    basename='tasks'
)
router.register(
    'taskitem',
    views.TaskItemViewSet,
    basename='taskitem'
)
router.register(
    'taskitem/python38',
    views.Python38ViewSet,
    basename='taskitem-python38'
)
router.register(
    'taskitem/gcc74',
    views.GCC74ViewSet,
    basename='taskitem-gcc74'
)
router.register(
    'taskitem/prolog-d',
    views.PrologDViewSet,
    basename='taskitem-prolog-d'
)
router.register(
    'taskitem/postgresql',
    views.PostgresqlViewSet,
    basename='taskitem-postgresql'
)
router.register(
    'taskitem/pascal',
    views.PascalViewSet,
    basename='taskitem-pascal'
)
router.register(
    'taskitem/php',
    views.PhpViewSet,
    basename='taskitem-php'
)
router.register(
    'taskitem/csharp',
    views.CSharpViewSet,
    basename='taskitem-csharp'
)
router.register(
    'taskitem/java',
    views.JavaViewSet,
    basename='taskitem-java'
)


urlpatterns = router.urls
