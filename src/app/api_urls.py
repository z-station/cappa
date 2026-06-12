from django.urls import path, include

urlpatterns = [
    path('translators/', include('app.translators.api.urls')),
    path('training/', include('app.training.api.urls')),
    path('groups/', include('app.groups.api.urls')),
    path('tasks/', include('app.tasks.api.urls')),
]
