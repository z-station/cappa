from rest_framework.permissions import BasePermission


class TeacherPermission(BasePermission):

    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.is_authenticated and user.is_teacher:
            return True
        return False
