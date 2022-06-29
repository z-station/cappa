from django.core.exceptions import PermissionDenied


def teacher_access(function):
    def wrapper(request, *args, **kw):
        user = request.user
        if user.is_authenticated and user.is_teacher:
            return function(request, *args, **kw)
        else:
            raise PermissionDenied()
    return wrapper
