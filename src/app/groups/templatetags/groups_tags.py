from django import template

register = template.Library()


@register.inclusion_tag('groups/parts/breadcrumbs.html')
def show_breadcrumbs(obj):
    return {'object': obj}

