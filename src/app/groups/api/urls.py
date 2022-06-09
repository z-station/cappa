from rest_framework.routers import DefaultRouter
from app.groups.api.views import GroupViewSet

router = DefaultRouter()
router.register('', viewset=GroupViewSet, basename='groups')

urlpatterns = router.urls
