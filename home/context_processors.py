#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from .models import User, Developer
def front_user(request):
    user_id = request.session.get('user_id')
    deve_id = request.session.get('deve_id')
    context = {}
    if user_id:
        try:
            user = User.objects.get(pk=user_id)
            context['front_user'] = user
        except:
            pass
    if deve_id:
        try:
            user = Developer.objects.get(pk=deve_id)
            context['front_user'] = user
        except:
            pass
    return context