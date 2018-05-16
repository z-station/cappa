# -*- coding: utf-8 -*-
from django.views.generic import DetailView, TemplateView
from project.courses.models import TreeItem
from django.shortcuts import get_object_or_404



class CatalogRootView(TemplateView):
    """
    Render courses root page
    """
    template_name = 'courses/root.html'



    def get_context_data(self, **kwargs):
        context = super(CatalogRootView, self).get_context_data(**kwargs)
        context['courses'] = TreeItem.objects.filter(show=True, level=0)
        return context


class CatalogItemView(DetailView):
    """
    Render courses page for object
    """
    template_name = "courses/treeitem.html"

    def get_object(self, queryset=None):
        path = self.kwargs.get('path', None)
        if path.endswith('/'):
            path = path[:-1]
        slug = path.split('/')[-1]
        item = get_object_or_404(TreeItem, slug=slug)
        return item
