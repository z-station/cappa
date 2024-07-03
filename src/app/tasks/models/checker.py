from django.db import models
from django.contrib.auth import get_user_model


UserModel = get_user_model()


class Checker(models.Model):

    class Meta:
        verbose_name = "чекер"
        verbose_name_plural = "чекеры"
        ordering = ('name',)

    name = models.CharField(
        verbose_name="заголовок",
        max_length=255
    )
    description = models.TextField(verbose_name="описание")
    content = models.TextField(
        verbose_name="Функция сверки решения",
        help_text="def checker(right_value: str, value: str) -> bool:"
    )

    def __str__(self):
        return self.name
