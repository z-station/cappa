from rest_framework.routers import DefaultRouter
from app.translators.api.views import (
    Python38ViewSet,
    PrologDViewSet,
    GCC74ViewSet,
    PostgresqlViewSet,
    PascalViewSet,
    PhpViewSet,
    CSharpViewSet,
    JavaViewSet,
    Rust186ViewSet,
    Go123ViewSet,
    Node20ViewSet,
    Java17ViewSet,
    Kotlin23ViewSet,
    Ruby4ViewSet,
    Python314ViewSet,
)

router = DefaultRouter()
router.register('python38', Python38ViewSet, basename='python38')
router.register('gcc74', GCC74ViewSet, basename='gcc74')
router.register('prolog-d', PrologDViewSet, basename='prolog-d')
router.register('postgresql', PostgresqlViewSet, basename='postgresql')
router.register('pascal', PascalViewSet, basename='pascal')
router.register('php', PhpViewSet, basename='php')
router.register('csharp', CSharpViewSet, basename='csharp')
router.register('java', JavaViewSet, basename='java')
router.register('rust186', Rust186ViewSet, basename='rust186')
router.register('go123', Go123ViewSet, basename='go123')
router.register('node20', Node20ViewSet, basename='node20')
router.register('java17', Java17ViewSet, basename='java17')
router.register('kotlin23', Kotlin23ViewSet, basename='kotlin23')
router.register('ruby4', Ruby4ViewSet, basename='ruby4')
router.register('python314', Python314ViewSet, basename='python314')

urlpatterns = router.urls
