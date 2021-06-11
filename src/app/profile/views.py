from django.views.generic import View
from django.shortcuts import render, redirect
from app.profile.forms import SignInForm, SignupForm
from django.contrib.auth import login, logout as auth_logout
from app.service.models.site import SiteSettings
from app.profile.mixins import NextPathMixin


class SignInView(View, NextPathMixin):

    def get(self, request, *args, **kwargs):
        if request.user.is_active:
            return redirect('/')
        next_path = self._get_next_path(request)
        form = SignInForm(
            request=request,
            initial={'next': next_path}
        )
        signup_path = '/signup/'
        if next_path != self.HOME_PATH:
            signup_path += f'?next={next_path}'
        return render(
            request=request,
            template_name='profile/login.html',
            context={
                'form': form,
                'signup_path': signup_path
            }
        )

    def post(self, request, *args, **kwargs):
        form = SignInForm(request=request, data=request.POST)
        if form.is_valid():
            login(request, form.user)
            return redirect(form.cleaned_data.get('next', '/'))
        else:
            return render(
                request=request,
                template_name='profile/login.html',
                context={'form': form}
            )


class SignOutView(View, NextPathMixin):

    def get(self, request, *args, **kwargs):
        auth_logout(request)
        next_path = self._get_next_path(request)
        if next_path != self.HOME_PATH:
            return redirect(next_path)
        else:
            return redirect(self.HOME_PATH)


class SignUpView(View, NextPathMixin):

    def get(self, request, *args, **kwargs):
        if request.user.is_active:
            return redirect(self.HOME_PATH)
        next_path = self._get_next_path(request)
        form = SignupForm(initial={'next': next_path})
        signin_path = '/signin/'
        if next_path != self.HOME_PATH:
            signin_path += f'?next={next_path}'
        return render(
            request=request,
            template_name='profile/signup.html',
            context={
                'form': form,
                'signin_path': signin_path
            }
        )

    def post(self, request, *args, **kwargs):
        form = SignupForm(data=request.POST)
        if form.is_valid():
            site_settings = SiteSettings.objects.last()
            if site_settings.confirm_signup:
                user = form.save(commit=False)
                user.is_active = False
                user.save()
            else:
                user = form.save()
                login(request, user)
            return redirect(form.cleaned_data.get('next', self.HOME_PATH))
        else:
            return render(
                request=request,
                template_name='profile/signup.html',
                context={'form': form}
            )

