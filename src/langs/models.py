from django.db import models
from . import providers


class Lang(models.Model):

    class Meta:
        verbose_name = "язык программирования"
        verbose_name_plural = "языки программирования"

    PYTHON = "python"
    CPP = "cpp"
    CSHARP = "csharp"
    PROVIDERS_CHOICES = (
        (PYTHON, "Python 3.6"),
        (CPP, "C++"),
        (CSHARP, "C#"),
    )

    provider = models.CharField(
        verbose_name="заголовок", max_length=255,
        choices=PROVIDERS_CHOICES, unique=True
    )

    def __str__(self):
        for choice in self.PROVIDERS_CHOICES:
            if choice[0] == self.provider:
                return choice[1]

    def debug(self, *args, **kwargs):
        return getattr(providers, self.provider).debug(*args, **kwargs)

    def tests(self, *args, **kwargs):
        return getattr(providers, self.provider).tests(*args, **kwargs)
