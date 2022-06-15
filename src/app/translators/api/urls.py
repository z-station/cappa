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

urlpatterns = router.urls
