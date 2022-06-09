from django.db import models
from django.contrib.auth import get_user_model


UserModel = get_user_model()


class Tag(models.Model):

    class Meta:
        verbose_name = "метка"
        verbose_name_plural = "метки"
        ordering = ('name',)

    name = models.CharField(verbose_name="имя", max_length=255)

    def __str__(self):
        return self.name
