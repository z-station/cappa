from allauth.account.views import LoginView, LogoutView, SignupView, ConfirmEmailView, \
    PasswordResetView, PasswordResetFromKeyView
from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404, redirect, HttpResponse, render

from project.executors.forms import CodeForm
from project.executors.models import Code, CodeTest, Executor, UserSolution
from project.executors.utils import create_or_update_solution


class MyLoginView(LoginView):
    template_name = 'allauth/account/login.html'


class MyLogoutView(LogoutView):
    template_name = 'allauth/account/logout.html'


class MySignupView(SignupView):
    template_name = 'allauth/account/signup.html'


class MyEmailVerifySentView(TemplateView):
    template_name = 'allauth/account/verification_sent.html'


class MyEmailConfirmView(ConfirmEmailView):
    template_name = 'allauth/account/email_confirm.html'


class MyPasswordResetView(PasswordResetView):
    template_name = 'allauth/account/password_reset.html'


class MyPasswordResetFromKeyView(PasswordResetFromKeyView):
    template_name = 'allauth/account/password_reset_from_key.html'


class MyPasswordResetDoneView(TemplateView):
    template_name = 'allauth/account/password_reset_done.html'


class PasswordResetFromKeyDoneView(TemplateView):
    template_name = 'allauth/account/password_reset_from_key_done.html'


def profile(request):
    pass
