# -*- coding: utf-8 -*-
from django import template


register = template.Library()


@register.assignment_tag(takes_context=True)
def get_admin_sidebar_models(context):

    """ Получить список ссылок для сайдбара в админке """

    user = context['request'].user
    data = []
    if user.is_superuser or user.has_perm('auth.add_user') or user.has_perm('auth.change_user'):
        data.append({'title': 'Пользователи', 'url': '/admin/accounts/user/'})
    if user.is_superuser or user.has_perm('auth.add_group') or user.has_perm('auth.change_group'):
        data.append({'title': 'Группы', 'url': '/admin/auth/group/'})
    if user.is_superuser or user.has_perm('service.add_sitesettings') or user.has_perm('service.change_sitesettings'):
        data.append({'title': 'Сайты', 'url': '/admin/service/sitesettings/'})
    return data


@register.filter
def cut_zero(float_val):
    try:
        return float_val if float_val % 1 else int(float_val)
    except TypeError:
        return float_val


@register.inclusion_tag('common/breadcrumbs.html')
def show_breadcrumbs(obj):
    return {'object': obj}


@register.inclusion_tag('common/pagination.html', takes_context=True)
def show_pagination(context, page):
    get_copy = context['request'].GET.copy()
    query_params = get_copy.pop('page', True) and get_copy.urlencode()
    return {
        'page': page,
        'query_params': query_params
    }
