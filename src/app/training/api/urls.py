from rest_framework.routers import DefaultRouter
from app.training.api.views import (
    CourseViewSet,
)

router = DefaultRouter()

router.register('courses', CourseViewSet, basename='courses')

urlpatterns = router.urls
