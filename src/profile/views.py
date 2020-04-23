from django.views.generic import View
from django.shortcuts import HttpResponse, render, redirect
from src.profile.forms import LoginForm, SignupForm
from django.contrib.auth import login, logout as auth_logout
from urllib import parse


class LoginView(View):

    def get(self, request, *args, **kwargs):
        if request.user.is_active:
            return redirect('/')
        next = parse.urlparse(request.META.get('HTTP_REFERER', '/')).path
        return render(
            request=request,
            template_name='profile/login.html',
            context={'form': LoginForm(request=request, initial={'next': next})}
        )

    def post(self, request, *args, **kwargs):
        form = LoginForm(request=request, data=request.POST)
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
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            return redirect(form.cleaned_data.get('next', '/'))
        else:
            return render(
                request=request,
                template_name='profile/signup.html',
                context={'form': form}
            )

