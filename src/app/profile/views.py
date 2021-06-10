from django.views.generic import View
from django.shortcuts import render, redirect
from app.profile.forms import SignInForm, SignupForm
from django.contrib.auth import login, logout as auth_logout
from app.service.models.site import SiteSettings
from urllib import parse


class SignInView(View):

    def get(self, request, *args, **kwargs):
        if request.user.is_active:
            return redirect('/')
        next = parse.urlparse(request.META.get('HTTP_REFERER', '/')).path
        return render(
            request=request,
            template_name='profile/login.html',
            context={'form': SignInForm(request=request, initial={'next': next})}
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


def logout(request, *args, **kwargs):
    # TODO оставлять на той же странице, если есть права, иначе на главную
    # next = parse.urlparse(request.META.get('HTTP_REFERER', '/')).path
    auth_logout(request)
    return redirect('/')


class SignUpView(View):

    def get(self, request, *args, **kwargs):
        if request.user.is_active:
            return redirect('/')
        next = parse.urlparse(request.META.get('HTTP_REFERER', '/')).path
        return render(
            request=request,
            template_name='profile/signup.html',
            context={'form': SignupForm(initial={'next': next})}
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
            return redirect(form.cleaned_data.get('next', '/'))
        else:
            return render(
                request=request,
                template_name='profile/signup.html',
                context={'form': form}
            )

