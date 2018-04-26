from django import forms
from django.template import loader
from django.utils import formats


class AceEditorWidget(forms.Widget):

    template_name = 'ace/widget.html'

    def value_from_datadict(self, data, files, name):
        return data.get(name)

    def render(self, name, value, attrs=None, renderer=None):
        context = self.get_context(name, value, attrs)
        return loader.render_to_string(self.template_name, context)
