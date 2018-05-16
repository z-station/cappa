# -*- coding: utf-8 -*-
from django.conf.urls import url
from project.courses.views import CatalogRootView, CatalogItemView

urlpatterns = [
    url(r'^$', CatalogRootView.as_view(), name='courses-root'),
    url(r'^(?P<path>.*)/$', CatalogItemView.as_view(), name='courses-item'),
]