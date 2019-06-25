from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    group = models.CharField(max_length=25, verbose_name='Группа', blank=True)
    team = models.CharField(max_length=50, verbose_name='Команда', blank=True)
    university = models.CharField(max_length=100, verbose_name='Университет', blank=True)


