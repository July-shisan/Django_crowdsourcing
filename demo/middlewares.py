#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from demo.models import User

REQUIRE_LOGIN = [
    '/release/',
]
class FrontUserMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response
    # def process_request(self, request):
    #     print('---------')
    # def process_response(self, request, response):
    #     return response
    def __call__(self, request):
        if request.path in REQUIRE_LOGIN:
            user_id = request.session.get('user_id')
            if user_id:
                try:
                    user = User.objects.get(pk=user_id)
                    request.front_user = user
                except:
                    return redirect(reverse('login'))
            else:
                messages.success(request, "Log In First!")
                return redirect(reverse('login'))
        response = self.get_response(request)
        return response
