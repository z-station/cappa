from django import forms
from django.core.exceptions import ValidationError
from src.training.models import Topic, Content
from src.widgets.ace import AceWidget
from .utils import Response


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
            'admin/training/topic.js'
        ]
        css = {
            'all': ['admin/training/topic.css']
        }


class ContentForm(forms.Form):

    input = forms.CharField(label="Консольный ввод", required=False)
    content = forms.CharField(label='')
    output = forms.CharField(
        label="Вывод", required=False,
        widget=forms.Textarea(attrs={'readonly': True})
    )
    error = forms.CharField(
        label="Ошибка", required=False,
        widget=forms.Textarea(attrs={'readonly': True})
    )
    operation = forms.CharField(widget=forms.Select(choices='Operations.CHOICES'))
    lang = forms.CharField(widget=forms.HiddenInput)

    def perform_operation(self, topic):
        if self.is_valid():
            return getattr(self.Operations, self.cleaned_data['operation'])(self.cleaned_data, topic)
        else:
            return Response(status=401, msg='Некорректные данные формы')

    class Operations:

        CHOICES = (
            ('debug', 'debug'),
        )

        @staticmethod
        def debug(data, topic):
            result = topic.lang.provider.debug(data['input'], data['content'])
            if result['error']:
                return Response(status=400, msg='Ошибка отладки', output=result['output'], error=result['error'])
            else:
                return Response(status=200, msg='Готово', output=result['output'])
