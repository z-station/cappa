from rest_framework.routers import DefaultRouter
from app.translators.api.views import (
    Python38ViewSet,
    PrologDViewSet,
    GCC74ViewSet
)

router = DefaultRouter()
router.register('python38', Python38ViewSet, basename='python38')
router.register('gcc74', GCC74ViewSet, basename='gcc74')
router.register('prolog-d', PrologDViewSet, basename='prolog-d')

urlpatterns = router.urls
