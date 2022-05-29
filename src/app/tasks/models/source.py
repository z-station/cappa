from django.db import models
from django.contrib.auth import get_user_model


UserModel = get_user_model()


class Source(models.Model):

    class Meta:
        verbose_name = "внешний источник"
        verbose_name_plural = "внешние источники"
        ordering = ('name',)

    name = models.CharField(
        verbose_name="название",
        max_length=255
    )
    description = models.TextField(
        verbose_name="описание",
        blank=True,
        null=True
    )

    def __str__(self):
        return self.name
