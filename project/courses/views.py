# -*- coding: utf-8 -*-
from django.views.generic import DetailView, TemplateView
from project.courses.models import TreeItem
from django.http import Http404


class CatalogRootView(TemplateView):
    """ Срендерить корневую страницу курсов """
    template_name = 'courses/root.html'

    def get_context_data(self, **kwargs):
        context = super(CatalogRootView, self).get_context_data(**kwargs)
        context['courses'] = TreeItem.objects.filter(show=True, level=0)
        return context


class CatalogItemView(DetailView):
    """ Идентифицировать по url элемент курса и срендерить его
        или вернуть 404 """
    template_name = "courses/treeitem.html"

    def get_object(self, queryset=None):
        path = self.kwargs.get('path', None)
        if path.endswith('/'):
            path = path[:-1]
        slug = path.split('/')[-1]
        items = TreeItem.objects.filter(slug=slug)
        if items.exists():
            if len(items) == 1:
                return items[0]
            else:
                for item in items:
                    if item.get_complete_slug() == path:
                        return item
        return Http404
