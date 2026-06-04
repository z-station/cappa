
class PermissionMixin:
    """
    Проверка доступа к class-based view.

    1. Определите класс permission с методом has_permission(request, view, user=None)
       и при необходимости атрибутом message — текст ошибки для пользователя.
    2. Унаследуйте view от PermissionMixin.
    3. Задайте permission_classes — permissions для всех HTTP-методов.
    4. При необходимости задайте action_permissions — permissions для отдельных
       методов (ключ — имя метода в нижнем регистре: get, post, put, ...).
       Permissions из action_permissions проверяются дополнительно к permission_classes.
    5. В get/post вызывайте check_permissions(request) и обрабатывайте отказ во view.

    Пример::

        class SignUpView(PermissionMixin, View):

            permission_classes = (SignUpPermission,)

            def get(self, request, *args, **kwargs):
                denied_permission = self.check_permissions(request)
                if denied_permission is not None:
                    return render(..., {'error_message': denied_permission.message})

        class SignInView(PermissionMixin, View):

            action_permissions = {'post': (SignInPermission,)}
    """

    permission_classes = ()
    action_permissions = {}

    def get_permission_classes(self, request):
        permission_classes = list(self.permission_classes)
        method_permissions = self.action_permissions.get(request.method.lower())
        if method_permissions is not None:
            permission_classes.extend(method_permissions)
        return permission_classes

    def get_permissions(self, request):
        return [permission() for permission in self.get_permission_classes(request)]

    def check_permissions(self, request, user=None):
        for permission in self.get_permissions(request):
            if not permission.has_permission(request, self, user=user):
                return permission
        return None
