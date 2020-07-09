#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from .models import User
def front_user(request):
    user_id = request.session.get('user_id')
    context = {}
    if user_id:
        try:
            user = User.objects.get(pk=user_id)
            context['front_user'] = user
        except:
            pass
    return context