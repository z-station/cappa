
class GroupStatus:

    OPEN = '0'
    CLOSED = '1'
    BY_CODEWORD = '2'
    CHOICES = (
        (OPEN, 'открыто'),
        (CLOSED, 'закрыто'),
        (BY_CODEWORD, 'по кодовому слову'),
    )
    MAP = {
        OPEN: 'открыто',
        CLOSED: 'закрыто',
        BY_CODEWORD: 'по кодовому слову',
    }


class GroupMemberRole:

    TEACHER = 'teacher'
    LEARNER = 'learner'

    CHOICES = (
        (TEACHER, 'Преподаватель'),
        (LEARNER, 'Ученик'),
    )


class GroupCourseStatisticAccess:

    ONLY_FOR_TEACHERS = 'only_for_teachers'
    ALLOW_FOR_ALL = 'allow_for_all'
    CLOSED = 'closed'

    CHOICES = (
        (ONLY_FOR_TEACHERS, 'Для преподавателей'),
        (ALLOW_FOR_ALL, 'Для преподавателей и учеников'),
        (CLOSED, 'закрыт'),
    )
