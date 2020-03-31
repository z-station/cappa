from datetime import datetime
from django import template

register = template.Library()


@register.filter
def date_format(str_datetime):
    if str_datetime:
        val = datetime.strptime(str_datetime, '%Y-%m-%d %H:%M:%S.%f')
        return val.strftime('%Y.%m.%d: %H:%M')
    else:
        return '-'


@register.inclusion_tag('training/parts/breadcrumbs.html')
def show_breadcrumbs(obj):
    return {'object': obj}


@register.inclusion_tag('training/parts/sidebar.html', takes_context=True)
def show_sidebar(context, course):
    context['data'] = course.get_cache_data()
    return context


@register.filter
def cut_zero(float_val):
    try:
        return float_val if float_val % 1 else int(float_val)
    except TypeError:
        return float_val
