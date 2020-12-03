# -*- coding: utf-8 -*-
from django import template


register = template.Library()


@register.assignment_tag(takes_context=True)
def get_admin_sidebar_models(context):

    """ Получить список ссылок для сайдбара в админке """

    user = context['request'].user
    data = []
    if user.is_superuser or user.has_perm('auth.add_user') or user.has_perm('auth.change_user'):
        data.append({'title': 'Пользователи', 'url': '/admin/auth/user/'})
    if user.is_superuser or user.has_perm('auth.add_group') or user.has_perm('auth.change_group'):
        data.append({'title': 'Группы', 'url': '/admin/auth/group/'})
    if user.is_superuser or user.has_perm('service.add_sitesettings') or user.has_perm('service.change_sitesettings'):
        data.append({'title': 'Сайты', 'url': '/admin/service/sitesettings/'})
    return data

