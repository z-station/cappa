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

translators_hosts = {
    PYTHON38: settings.PYTHON38_HOST,
    GCC74: settings.GCC75_HOST,
}
