from django.contrib.auth.models import UserManager
from app.accounts.querysets import UserQuerySet


class CustomUserManager(UserManager.from_queryset(UserQuerySet)):

    pass
