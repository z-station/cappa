from django import forms
from allauth.account.forms import SignupForm, LoginForm, PasswordField
from allauth import app_settings


class CustomSignupForm(SignupForm):

    username = forms.CharField(
        label='логин',
        min_length=4,
        widget=forms.TextInput(attrs={'placeholder': 'логин', 'autofocus': 'autofocus'})
    )
    email = forms.EmailField(
        label='e-mail',
        widget=forms.TextInput(attrs={'type': 'email', 'placeholder': 'e-mail '})
    )
    first_name = forms.CharField(
        label="имя",
        widget=forms.TextInput(attrs={'placeholder': 'имя'})
    )
    last_name = forms.CharField(
        label="фамилия",
        widget=forms.TextInput(attrs={'placeholder': 'фамилия'})
    )


class CustomLoginForm(LoginForm):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(forms.Form, self).__init__(*args, **kwargs)

    login = forms.CharField(
        label='Логин или e-mail',
        widget= forms.TextInput(
            attrs={'placeholder': 'Логин или e-mail', 'autofocus': 'autofocus'}
        )
    )

    password = PasswordField(label='Пароль')
    remember = forms.BooleanField(label="Запомнить меня", required=False)
