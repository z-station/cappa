from app.accounts.enums import UserRole
from app.service.enums import SiteAccessType
from app.service.models.site import SiteSettings


class SignInPermission:

    message = 'Авторизация временно отключена администратором'

    def get_access_type(self):
        site_settings = SiteSettings.objects.last()
        if site_settings is None:
            return SiteAccessType.ALL
        return site_settings.signin

    def user_is_allowed(self, user):
        if user.is_superuser:
            return True
        access_type = self.get_access_type()
        if access_type == SiteAccessType.ALL:
            return True
        if access_type == SiteAccessType.TEACHER:
            return user.role == UserRole.TEACHER
        if access_type == SiteAccessType.SUPERUSER:
            return user.is_superuser
        return True

    def has_permission(self, request, view, user=None):
        if user is None:
            return True
        return self.user_is_allowed(user)


class SignUpPermission:

    message = 'Регистрация новых пользователей временно отключена администратором'

    def has_permission(self, request, view, user=None):
        site_settings = SiteSettings.objects.last()
        if site_settings is None:
            return True
        return site_settings.signup
