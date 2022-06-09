from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from app.accounts.models import User
from app.groups.admin import UserGroupInline


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
    list_filter = ('is_active', 'role', 'groups')
    search_fields = (
        'username',
        'first_name',
        'last_name',
        'father_name',
        'email'
    )
    inlines = (UserGroupInline, )


admin.site.register(User, UserAdmin)
