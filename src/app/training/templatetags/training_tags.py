from django import template
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string
from app.tasks.models import Draft
from app.training.models import (
    Content,
    Topic,
    TaskItem
)
from app.training.forms.topic import ContentForm
from app.training.forms.taskitem import EditorForm, SqlEditorForm


register = template.Library()


@register.inclusion_tag('training/parts/breadcrumbs.html')
def show_breadcrumbs(obj):
    return {'object': obj}


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


@register.simple_tag(takes_context=True)
def show_editor(context, taskitem: TaskItem):
    draft = Draft.objects.filter(
        task_id=taskitem.task_id,
        user_id=context.request.user.id,
        translator=taskitem.translator
    ).first()

    form = EditorForm(
        initial={
            'content': draft.content if draft else '',
            'input': '',
            'translator': taskitem.translator,
        }
    )
    show_testing_actions = (
        taskitem.score_method_is_tests
        or taskitem.score_method_is_tests_and_review
    )
    raw_html = render_to_string(
        template_name='training/parts/editor.html',
        context={
            'object': taskitem,
            'form': form,
            'show_testing_actions': show_testing_actions
        },
        request=context.request
    )
    return mark_safe(raw_html)


@register.simple_tag(takes_context=True)
def show_sql_editor(context, taskitem: TaskItem):
    draft = Draft.objects.filter(
        task_id=taskitem.task_id,
        user_id=context.request.user.id,
        translator=taskitem.translator
    ).first()

    form = SqlEditorForm(
        initial={
            'content': draft.content if draft else '',
            'translator': taskitem.translator,
            'db_name': taskitem.get_db_name()
        }
    )
    show_testing_actions = (
        taskitem.score_method_is_tests
        or taskitem.score_method_is_tests_and_review
    )
    raw_html = render_to_string(
        template_name='training/parts/sql/editor.html',
        context={
            'object': taskitem,
            'form': form,
            'show_testing_actions': show_testing_actions
        },
        request=context.request
    )
    return mark_safe(raw_html)
