from django import template
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string
from src.training.models import Content
from src.training.forms import ContentForm


register = template.Library()


@register.inclusion_tag('training/topic/parts/ace_field.html')
def show_ace_field(field):
    return {'field': field}


@register.simple_tag(takes_context=True)
def show_content(context, topic):
    raw_html = ''
    for content in topic._content.all():
        extra_context = {'content': content}
        if content.type == Content.ACE:
            extra_context['form'] = ContentForm(initial={
                'content': content.content,
                'input': content.input,
                'lang': content.lang.provider_name
            }, prefix=content.id)

        raw_html += render_to_string(
            template_name='training/topic/parts/content_%s.html' % content.type,
            context=extra_context,
            request=context.request
        )
    return mark_safe(raw_html)
