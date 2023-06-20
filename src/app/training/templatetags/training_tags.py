from django import template
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string
from app.training.models import (
    Content,
    Topic,
)
from app.training.forms.topic import ContentForm


register = template.Library()


@register.inclusion_tag('training/parts/sidebar.html', takes_context=True)
def show_sidebar(context, course):
    context['course'] = course.get_cache_data()
    return context


@register.inclusion_tag('training/parts/ace_field.html')
def show_ace_field(field):
    return {'field': field}


@register.simple_tag(takes_context=True)
def show_content(context, topic: Topic):
    raw_html = ''
    for obj in topic._content.all():
        extra_context = {'obj': obj}
        if obj.type == Content.ACE:
            extra_context['form'] = ContentForm(
                initial={
                    'content': obj.content,
                    'input': obj.input,
                    'translator': obj.translator,
                    'db_name': topic.get_db_name()
                },
                prefix=obj.id
            )

        raw_html += render_to_string(
            template_name='training/parts/content_%s.html' % obj.type,
            context=extra_context,
            request=context.request
        )
    return mark_safe(raw_html)
