from django.conf import settings

PYTHON38 = '1'
GCC74 = '2'

translators_ids = [
    PYTHON38,
    GCC74,
]

translators_choices = (
    (PYTHON38, 'Python 3.8'),
    (GCC74, 'GCC 7.5'),
)

translators_external_urls = {
    PYTHON38: settings.SERVICES["PYTHON38"]["EXTERNAL_URL"],
    GCC74: settings.SERVICES["GCC74"]["EXTERNAL_URL"]
}

translators_internal_urls = {
    PYTHON38: settings.SERVICES["PYTHON38"]["INTERNAL_URL"],
    GCC74: settings.SERVICES["GCC74"]["INTERNAL_URL"]
}
