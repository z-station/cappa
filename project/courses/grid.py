# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from django.contrib.admin.utils import display_for_field
from django.db.models.fields import FieldDoesNotExist
from django.core.urlresolvers import reverse
from mptt.templatetags.mptt_admin import get_empty_value_display
from django.core.exceptions import ObjectDoesNotExist
from django.utils.encoding import smart_text
from django.template.defaultfilters import linebreaksbr
from django.utils.safestring import mark_safe
from django.utils.html import conditional_escape
from django.db import models


class GridField(object):

    EDITABLE_FIELDS = [
        'CharField',
        'IntegerField',
        'PositiveIntegerField',
        'BooleanField'
    ]

    def __init__(self, obj, field_name, admin_cls):
        self.obj = obj
        self.field_name = field_name
        self.admin_cls = admin_cls

    def editable(self):
        """
        :return: True if field is editable else return False
        """
        editable = True
        try:
            field = self.obj._meta.get_field(self.field_name)
            if field.get_internal_type() not in self.EDITABLE_FIELDS or \
                    self.field_name not in self.admin_cls.list_editable:
                    editable = False
        except FieldDoesNotExist:
            editable = False
        return editable

    def contents(self):
        """
        :return: type, value and correct values of field
        """
        field_type = 'text'
        value = ''
        correct_values, modelfield = None, None
        if self.field_name in self.admin_cls.list_display:
            try:
                modelfield, attr, val = admin.utils.lookup_field(self.field_name, self.obj, self.admin_cls)
            except (AttributeError, ValueError, ObjectDoesNotExist):
                result_repr = get_empty_value_display(self.admin_cls)
            else:
                if modelfield is None:
                    boolean = getattr(attr, "boolean", False)
                    if boolean:
                        result_repr = 't' if val else 'f'
                        field_type = 'checkbox'
                    else:
                        result_repr = smart_text(val)
                        if getattr(attr, "allow_tags", False):
                            result_repr = mark_safe(result_repr)
                        else:
                            result_repr = linebreaksbr(result_repr,
                                                       autoescape=True)
                else:
                    result_repr = display_for_field(val, modelfield, " ")
            value = conditional_escape(result_repr)
            if modelfield:
                if isinstance(modelfield, models.BooleanField):
                    field_type = 'checkbox'
                    value = 't' if val else 'f'
                if isinstance(modelfield,
                              (models.IntegerField, models.CharField)) \
                        and modelfield.choices:
                    field_type = 'select'
                    value = val
                    correct_values = dict(modelfield.choices)
        return field_type, value, correct_values


class GridRow(object):

    def __init__(self, obj, fields, admin_cls):
        self.obj = obj
        self.fields = fields
        self.admin_cls = admin_cls

    def json_data(self):
        """
        :return: JSON with fields data of object
        """
        link = reverse('admin:courses_treeitem_change', args=(self.obj.id,))
        data = {'id': self.obj.id, 'link': link}
        for field_name in self.fields:
            field = GridField(self.obj, field_name, self.admin_cls)
            field_type, field_value, correct_values = field.contents()
            data[field_name] = {
                'type': field_type,
                'value': field_value,
                'editable': field.editable(),
                'correct_values': correct_values if correct_values else ''
            }
        return data