from django.db import models
from . import providers


class Lang(models.Model):

    class Meta:
        verbose_name = "язык программирования"
        verbose_name_plural = "языки программирования"

    PYTHON = "python"
    CPP = "cpp"
    CSHARP = "csharp"
    PROVIDERS_NAMES = [PYTHON, CPP, CSHARP]
    PROVIDERS_CHOICES = (
        (PYTHON, PYTHON),
        (CPP, CPP),
        (CSHARP, CSHARP),
    )

    name = models.CharField(verbose_name="имя", max_length=255)
    provider_name = models.CharField(
        verbose_name="провайдер", max_length=255,
        choices=PROVIDERS_CHOICES, unique=True
    )

    def __str__(self):
        return self.name

    @property
    def provider(self):
        ProviderCls = getattr(getattr(providers, self.provider_name), 'Provider')
        provider = ProviderCls()
        return provider
