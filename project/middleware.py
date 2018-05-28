# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect
from django.utils.deprecation import MiddlewareMixin


class LoginRequiredMiddleware(MiddlewareMixin):

    def process_request(self, request):
        if not request.user.is_authenticated():
            path = request.path_info.lstrip('/')
            if path != 'login/':
                return HttpResponseRedirect("/login/")
