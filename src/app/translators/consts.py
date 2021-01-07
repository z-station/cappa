from django.conf import settings

PYTHON38 = 1
GCC75 = 2

ts_ids = [
    PYTHON38,
    GCC75,
]

ts_choices = (
    (PYTHON38, 'Python 3.8'),
    (GCC75, 'GCC 7.5'),
)

ts_hosts = {
    PYTHON38: settings.PYTHON38_HOST,
    GCC75: settings.GCC75_HOST,
}
