import re
from django import forms
from django.core import validators, exceptions
from django.contrib.auth import authenticate, get_user_model, password_validation

UserModel = get_user_model()


class SignInForm(forms.Form):

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.login_type = None
        self.request = request
        self.user = None

    login = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'autofocus': True,
            'placeholder': 'Логин или e-mail',
            'class': 'form-control'
        }),
    )
    password = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'пароль',
                'class': 'form-control'
            },
            render_value=True
        ),
    )

    next = forms.CharField(widget=forms.HiddenInput, required=False)

    def clean_login(self):
        login = self.cleaned_data.get('login')
        if login is None:
            self.add_error(field='login', error='Заполните обязательные поля')
        try:
            validators.validate_email(login)
            self.login_type = 'email'
        except exceptions.ValidationError:
            self.login_type = 'username'
        return login

    def clean(self):
        login = self.cleaned_data.get('login')
        password = self.cleaned_data.get('password')

        if login is not None and password:
            if self.login_type == 'username':
                self.user = authenticate(request=self.request, username=login, password=password)
            else:
                self.user = authenticate(request=self.request, email=login, password=password)

            if self.user is None:
                self.add_error(
                    field=None,
                    error='Проверьте правильность написания логина и пароля'
                )
            else:
                if not self.user.is_active:
                    self.add_error(
                        field=None,
                        error='Учетная запись не активна'
                    )
        else:
            self.add_error(field=None, error='Заполните обязательные поля')

        return self.cleaned_data


class SignupForm(forms.ModelForm):

    class Meta:
        model = UserModel
        fields = ['username', 'first_name', 'last_name', 'email', 'next']

    username = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'autofocus': True,
            'placeholder': 'Логин',
            'class': 'form-control'
        }),
    )

    email = forms.EmailField(
        max_length=255,
        widget=forms.EmailInput(attrs={
            'placeholder': 'E-mail',
            'class': 'form-control'
        })
    )

    first_name = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'placeholder': 'Имя',
            'class': 'form-control'
        }),
    )

    last_name = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'placeholder': 'Фамилия',
            'class': 'form-control'
        }),
    )
    password1 = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Пароль',
                'class': 'form-control'
            },
            render_value=True
        ),
        validators=[
            validators.MinLengthValidator(
                limit_value=6, message="Пароль должен быть больше 5 символов"
            )
        ]
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Повторите пароль',
                'class': 'form-control',
            },
            render_value=True
        ),
        validators=[
            validators.MinLengthValidator(
                limit_value=6,
                message="Пароль должен быть больше 5 символов"
            )
        ],
        strip=False,
    )
    next = forms.CharField(widget=forms.HiddenInput, required=False)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            self.add_error(field=None, error='Пароли не совпадают')
        else:
            self.instance.username = self.cleaned_data.get('username')
            password_validation.validate_password(self.cleaned_data.get('password2'), self.instance)
        return password2

    def clean_username(self):
        value = self.cleaned_data.get('username')
        username_unavailable = UserModel.objects.filter(username=value).exists()
        if username_unavailable:
            self.add_error(
                field='username',
                error='Пользователь с таким логином уже существует'
            )

        if not re.match(r'^[\w.]+$', value):
            self.add_error(
                field='username',
                error="Логин должен содержать только цифры, буквы, "
                    "точку или символ подчеркивания")
        return value

    def clean_email(self):
        email_unavailable = UserModel.objects.filter(email=self.cleaned_data['email']).exists()
        if email_unavailable:
            self.add_error(field=None, error='Пользователь с такой почтой уже существует')
        return self.cleaned_data['email']

    def save(self, commit=True):
        user = super(SignupForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
