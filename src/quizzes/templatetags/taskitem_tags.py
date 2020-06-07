from django import template

register = template.Library()


@register.inclusion_tag('quizzes/taskitem/parts/ace_field.html')
def show_ace_field(field):
    return {'field': field}
