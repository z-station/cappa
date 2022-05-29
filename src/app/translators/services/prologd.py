from django.conf import settings
from app.translators.enums import TranslatorType
from app.translators.services.base import BaseTranslatorService


class PrologDService(BaseTranslatorService):

    SERVICE_HOST = settings.SERVICES_HOSTS[TranslatorType.PROLOG_D]
