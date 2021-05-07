from django.conf import settings
from dataclasses import dataclass


@dataclass
class Translator:

    PYTHON38 = '1'
    GCC74 = '2'

    ids = [
        PYTHON38,
        GCC74,
    ]

    choices = (
        (PYTHON38, 'Python 3.8'),
        (GCC74, 'С++ (GCC 7.5)'),
    )

    names = {
        PYTHON38: 'Python 3.8',
        GCC74: 'С++ (GCC 7.5)'
    }

    external_urls = {
        PYTHON38: settings.SERVICES["PYTHON38"]["EXTERNAL_URL"],
        GCC74: settings.SERVICES["GCC74"]["EXTERNAL_URL"]
    }

    internal_urls = {
        PYTHON38: settings.SERVICES["PYTHON38"]["INTERNAL_URL"],
        GCC74: settings.SERVICES["GCC74"]["INTERNAL_URL"]
    }
