from django import forms
from django.core.exceptions import ValidationError
from app.training.models import Topic, Content
from app.common.widgets import AceWidget


class TopicAdminForm(forms.ModelForm):

    class Meta:
        model = Topic
        fields = '__all__'
        widgets = {'course': forms.HiddenInput}

    def clean(self):
        slug = self.cleaned_data.get('slug')
        course = self.cleaned_data.get('course')
        if slug and course:
            qst = Topic.objects.filter(course=course, slug=slug)
            if self.instance:
                qst = qst.exclude(id=self.instance.id)
            if qst.exists():
                self.add_error('slug', ValidationError('Значение не уникально в рамках курса'))
        return self.cleaned_data


class ContentAdminForm(forms.ModelForm):

    class Meta:
        model = Content
        fields = '__all__'
        widgets = {
            'input': AceWidget,
            'content': AceWidget
        }

    class Media:
        js = [
            'js/ace-1.4.7/ace.js',
            'admin/ace_init.js',
            'admin/tinymce_init.js',
            'admin/training/topic.js'
        ]
        css = {
            'all': [
                'admin/training/topic.css',
                'admin/ace.css'
            ]
        }


class ContentForm(forms.Form):

    input = forms.CharField(
        label="Консольный ввод",
        required=False
    )
    content = forms.CharField(label='')
    output = forms.CharField(
        label="Консольный вывод",
        required=False,
        widget=forms.Textarea(attrs={'readonly': True})
    )
    error = forms.CharField(
        label="Ошибка",
        required=False,
        widget=forms.Textarea(attrs={'readonly': True})
    )
    translator = forms.CharField(widget=forms.HiddenInput)
    db_name = forms.CharField(widget=forms.HiddenInput)
