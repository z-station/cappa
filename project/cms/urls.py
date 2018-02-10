# -*- coding:utf-8 -*-

from django.conf.urls import url, include
from catalog.views import CatalogItemView, CatalogRootView


urlpatterns = [
    url(r'^$', CatalogRootView.as_view(), name='cms-root'),
    url(r'^(?P<path>.*)/$', CatalogItemView.as_view(), name='cms-item'),
]
