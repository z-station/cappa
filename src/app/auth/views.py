from django.views.generic import View
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout as auth_logout
from rest_framework.authtoken.models import Token
from app.auth.forms import SignInForm, SignupForm
from app.service.models.site import SiteSettings
from app.auth.mixins import NextPathMixin
from app.common.mixins import PermissionMixin
from app.auth.permissions import SignInPermission, SignUpPermission


class SignInView(PermissionMixin, View, NextPathMixin):

    permission_classes = ()
    action_permissions = {
        'post': (SignInPermission,),
    }

    def _get_signin_context(self, request, form):
        next_path = self._get_next_path(request)
        signup_path = '/auth/signup/'
        if next_path != self.HOME_PATH:
            signup_path += f'?next={next_path}'
        return {
            'form': form,
            'signup_path': signup_path,
        }

    def get(self, request, *args, **kwargs):
        if request.user.is_active:
            return redirect('/')
        next_path = self._get_next_path(request)
        form = SignInForm(request=request, initial={'next': next_path})
        return render(
            request=request,
            template_name='auth/signin.html',
            context=self._get_signin_context(request, form),
        )

    def post(self, request, *args, **kwargs):

        form = SignInForm(request=request, data=request.POST)
        if form.is_valid():
            denied_permission = self.check_permissions(request, user=form.user)
            if denied_permission:
                form.add_error(field=None, error=denied_permission.message)
            else:
                login(request, form.user)
                Token.objects.get_or_create(user=form.user)
                return redirect(form.cleaned_data.get('next', '/'))
        return render(
            request=request,
            template_name='auth/signin.html',
            context=self._get_signin_context(request, form),
        )


class SignOutView(View, NextPathMixin):

    def get(self, request, *args, **kwargs):
        auth_logout(request)
        next_path = self._get_next_path(request)
        if next_path != self.HOME_PATH:
            return redirect(next_path)
        else:
            return redirect(self.HOME_PATH)


class SignUpView(PermissionMixin, View, NextPathMixin):

    action_permissions = {
        'post': (SignUpPermission,),
    }

    def _get_signup_context(self, request, form):
        next_path = self._get_next_path(request)
        signin_path = '/auth/signin/'
        if next_path != self.HOME_PATH:
            signin_path += f'?next={next_path}'
        site_settings = SiteSettings.objects.last()
        confirm_signup = (
            site_settings.confirm_signup
            if site_settings is not None
            else False
        )
        return {
            'form': form,
            'signin_path': signin_path,
            'confirm_signup': confirm_signup,
        }

    def get(self, request, *args, **kwargs):
        if request.user.is_active:
            return redirect(self.HOME_PATH)
        next_path = self._get_next_path(request)
        form = SignupForm(initial={'next': next_path})
        return render(
            request=request,
            template_name='auth/signup.html',
            context=self._get_signup_context(request, form),
        )

    def post(self, request, *args, **kwargs):
        form = SignupForm(data=request.POST)
        denied_permission = self.check_permissions(request)
        if denied_permission:
            form.add_error(field=None, error=denied_permission.message)
        elif form.is_valid():
            site_settings = SiteSettings.objects.last()
            confirm_signup = (
                site_settings.confirm_signup
                if site_settings is not None
                else False
            )
            if confirm_signup:
                user = form.save(commit=False)
                user.is_active = False
                user.save()
                return redirect(form.cleaned_data.get('next', self.HOME_PATH))
            else:
                user = form.save()
                signin_permission = SignInPermission()
                if signin_permission.has_permission(request, view=self, user=user):
                    login(request, user)
                    Token.objects.create(user=user)
                    return redirect(form.cleaned_data.get('next', self.HOME_PATH))
                else:
                    form.add_error(field=None, error=signin_permission.message)
        return render(
            request=request,
            template_name='auth/signup.html',
            context=self._get_signup_context(request, form),
        )
