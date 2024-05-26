import random
from unidecode import unidecode
from django.utils.text import slugify
from django.db import models
from django import forms
from django.db.models.fields import CharField
from filebrowser.fields import (
    FileBrowseField,
    FileBrowseWidget,
    FileBrowseFormField,
)


class OrderField(models.PositiveIntegerField):

    def __init__(self, for_fields=None, *args, **kwargs):
        self.for_fields = for_fields
        super().__init__(*args, **kwargs)

    def pre_save(self, instance, add):
        if getattr(instance, self.attname) is None:
            # Значение пусто
            qst = self.model.objects.all()
            try:
                if self.for_fields:
                    # Фильтруем обьекты с такими же значениями полей
                    # перечисленных в for_fields
                    query = {
                        field: getattr(instance, field)
                        for field in self.for_fields
                    }
                    qst = qst.filter(**query)
                value = qst.latest(self.attname).order_key + 1
            except:
                value = 1
            setattr(instance, self.attname, value)
            return value
        else:
            return super().pre_save(instance, add)


class TaskItemSlugField(models.SlugField):

    """ Added attribute "for_fields"
        and automatic slug filling from the task title """

    def __init__(self, for_fields=None, *args, **kwargs):
        self.for_fields = for_fields
        super().__init__(*args, **kwargs)

    def pre_save(self, instance, add):
        value = slugify(unidecode(instance.task.title))
        if self.for_fields:
            query = {
                field: getattr(instance, field)
                for field in self.for_fields
            }
            query['slug'] = value
            qst = self.model.objects.filter(**query)
            if instance.id:
                qst = qst.exclude(id=instance.id)
            if qst.exists():
                value += str(random.randint(0, 999))
        setattr(instance, self.attname, value)
        return value


class AnyExtFileBrowseFormField(FileBrowseFormField):

    def clean(self, value):
        value = super(forms.CharField, self).clean(value)
        return value


class AnyExtFileBrowseField(FileBrowseField):

    def formfield(self, **kwargs):
        widget_class = kwargs.get('widget', FileBrowseWidget)
        attrs = {}
        attrs["filebrowser_site"] = self.site
        attrs["directory"] = self.directory
        attrs["extensions"] = self.extensions
        attrs["format"] = self.format
        defaults = {
            'form_class': FileBrowseFormField,
            'widget': widget_class(attrs=attrs),
            'filebrowser_site': self.site,
            'directory': self.directory,
            'extensions': self.extensions,
            'format': self.format
        }
        return super(CharField, self).formfield(**defaults)
