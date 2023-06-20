from django import template
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string
from app.tasks.models import Draft, TaskItem
from app.tasks.forms import (
    EditorForm,
    SqlEditorForm,
)
from app.translators.enums import TranslatorType


register = template.Library()


@register.inclusion_tag('training/parts/ace_field.html')
def show_ace_field(field):
    return {'field': field}


@register.simple_tag(takes_context=True)
def show_editor(
    context,
    taskitem: TaskItem,
):
    translator = context['translator']
    draft = Draft.objects.filter(
        task_id=taskitem.task_id,
        user_id=context.request.user.id,
        translator=translator
    ).first()
    if translator == TranslatorType.POSTGRESQL:
        form = SqlEditorForm(
            initial={
                'content': draft.content if draft else '',
                'translator': translator,
                'db_name': taskitem.get_db_name()
            }
        )
    else:
        form = EditorForm(
            initial={
                'content': draft.content if draft else '',
                'input': '',
                'translator': translator,
            }
        )
    show_testing_actions = (
        taskitem.score_method_is_tests
        or taskitem.score_method_is_tests_and_review
    )
    raw_html = render_to_string(
        template_name='tasks/taskitem/parts/editor.html',
        context={
            'object': taskitem,
            'form': form,
            'show_testing_actions': show_testing_actions
        },
        request=context.request
    )
    return mark_safe(raw_html)
