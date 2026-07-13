from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from app.accounts.models import User
from app.groups.admin import UserGroupInline
from app.accounts.services import UserService


class OnlineFilter(admin.SimpleListFilter):
    title = 'Онлайн'
    parameter_name = 'is_online'

    def lookups(self, request, model_admin):
        return (
            ('1', 'Да'),
            ('0', 'Нет'),
        )

    def queryset(self, request, queryset):
        if self.value() == '1':
            queryset = queryset.filter(
                id__in=UserService.get_online_users_ids()
            )
        if self.value() == '0':
            queryset = queryset.exclude(
                id__in=UserService.get_online_users_ids()
            )
        return queryset


class UserAdmin(BaseUserAdmin):

    def full_name(self, obj):
        return f'{obj.last_name} {obj.first_name} {obj.father_name}'
    full_name.short_description = 'Пользователь'

    def is_online(self, obj):
        return obj.is_online
    is_online.short_description = 'Онлайн'
    is_online.boolean = True

    fieldsets = (
        (
            'Персональная информация',
            {
                'fields': (
                    'first_name',
                    'last_name',
                    'father_name',
                    'email',
                    'username',
                    'password',
                    'role',
                    'is_active',
                    'is_staff',
                    'is_superuser',
                )
            }
        ),
        (
            'Активность',
            {
                'fields': (
                    'last_login',
                    'date_joined',
                    'is_online',
                )
            }
        ),
        (
            'Права доступа',
            {
                'classes': ('collapse', 'closed'),
                'fields': (
                    'groups',
                    'user_permissions'
                )
           }
        ),

    )
    readonly_fields = ('last_login', 'date_joined', 'is_online')
    list_display = ('full_name', 'email', 'is_online', 'is_active',)
    list_filter = (OnlineFilter, 'is_active', 'role', 'groups', 'is_superuser', 'is_staff')
    search_fields = (
        'username',
        'first_name',
        'last_name',
        'father_name',
        'email'
    )
    inlines = (UserGroupInline, )


admin.site.register(User, UserAdmin)
