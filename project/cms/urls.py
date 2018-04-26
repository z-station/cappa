# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf.urls import url
from catalog.views import CatalogRootView, CatalogItemView


urlpatterns = [
    url(r'^$', CatalogRootView.as_view(), name='cms-root'),
    url(r'^(?P<path>.*)/$', CatalogItemView.as_view(), name='cms-item'),
]