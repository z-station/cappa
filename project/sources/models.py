from django.db import models


class Source(models.Model):
    class Meta:
        verbose_name = "источник"
        verbose_name_plural = "источники"

    name = models.CharField(verbose_name="наименование", max_length=255)

    def __str__(self):
        return self.name
