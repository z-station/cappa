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
router.register(
    'taskitem/rust186',
    views.Rust186ViewSet,
    basename='taskitem-rust186'
)
router.register(
    'taskitem/go123',
    views.Go123ViewSet,
    basename='taskitem-go123'
)
router.register(
    'taskitem/node20',
    views.Node20ViewSet,
    basename='taskitem-node20'
)
router.register(
    'taskitem/java17',
    views.Java17ViewSet,
    basename='taskitem-java17'
)
router.register(
    'taskitem/kotlin23',
    views.Kotlin23ViewSet,
    basename='taskitem-kotlin23'
)
router.register(
    'taskitem/ruby4',
    views.Ruby4ViewSet,
    basename='taskitem-ruby4'
)
router.register(
    'taskitem/python314',
    views.Python314ViewSet,
    basename='taskitem-python314'
)


urlpatterns = router.urls
