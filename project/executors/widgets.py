from django import forms
from django.template import loader


class AceEditorAdminWidget(forms.Widget):

    template_name = 'ace/widget_admin.html'

    def value_from_datadict(self, data, files, name):
        return data.get(name)

    def render(self, name, value, attrs=None, renderer=None):
        self.attrs.update(attrs)
        context = self.get_context(name, value, self.attrs)
        return loader.render_to_string(self.template_name, context)
