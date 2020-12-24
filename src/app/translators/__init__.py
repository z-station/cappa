from os.path import join
from os import makedirs
from django.conf import settings
from app.translators.enums import Translator

for translator in Translator:
    path = join(settings.TMP_DIR, translator.value)
    makedirs(path, exist_ok=True, mode=0o775)
