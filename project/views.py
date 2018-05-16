# -*- coding:utf-8 -*-
from django.shortcuts import redirect


def frontpage(request):
    return redirect("/courses/")
