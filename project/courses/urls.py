# -*- coding: utf-8 -*-
from django.conf.urls import url
from project.courses.views import CatalogRootView, catalog_item

urlpatterns = [
    url(r'^$', CatalogRootView.as_view(), name='courses-root'),
    url(r'^(?P<path>.*)/$', catalog_item, name='courses-item'),
]