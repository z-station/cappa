from django.urls import path
from app.tasks.views import (
    SolutionView,
    SolutionsView,
    SolutionsDiffView,
)

app_name = 'solutions'

urlpatterns = [
    path(
        '<int:pk>/diff/<int:pair>/',
        SolutionsDiffView.as_view(),
        name='diff'
    ),
    path('<int:pk>/', SolutionView.as_view(), name='solution'),
    path('', SolutionsView.as_view(), name='solutions'),
]
