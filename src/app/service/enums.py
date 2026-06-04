

class SiteAccessType:

    ALL = 'all'
    TEACHER = 'teacher'
    SUPERUSER = 'superuser'

    CHOICES = (
        (ALL, 'Всем'),
        (TEACHER, 'Только преподавателям'),
        (SUPERUSER, 'Только суперпользователям'),
    )
