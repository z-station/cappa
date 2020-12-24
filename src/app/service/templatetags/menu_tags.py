# -*- coding utf-8 -*-
from django import template
from django.template.loader import render_to_string
from app.service.models import Menu
from django.core.exceptions import ObjectDoesNotExist

register = template.Library()


@register.simple_tag
def show_menu(key):
    try:
        obj = Menu.objects.get(key=key)
    except ObjectDoesNotExist:
        obj = None
    return render_to_string(
        template_name=f'service/menu/{key}.html',
        context={"object": obj}
    )
