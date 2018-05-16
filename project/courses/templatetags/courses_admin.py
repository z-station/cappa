from django.core.urlresolvers import reverse
from django.template import Library

register = Library()


@register.inclusion_tag('admin/courses/include/add_btns.html')
def add_btns():
    """
    Get add object buttons for every registered courses models
    """
    models_info = []
    models_info.append([reverse('admin:courses_treeitem_add'), "treeitem"])
    return {'models_info': models_info, }