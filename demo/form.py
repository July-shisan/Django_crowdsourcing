#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from django import forms
from .models import User, Challenge
import datetime

class registerForm(forms.ModelForm):
    password_confirmation = forms.CharField()
    email = forms.EmailField(required=False)
    def clean(self):
        cleaned_data = super(registerForm, self).clean()
        password = cleaned_data.get('password')
        password_confirmation = cleaned_data.get('password_confirmation')
        if password != password_confirmation:
            raise forms.ValidationError(message="两次密码输入不一致")
        return cleaned_data
    class Meta:
        model = User
        # fields = "__all__"
        fields = {'username', 'password', 'email'}

class loginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = {'username', 'password'}

class challengeForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super(challengeForm, self).clean()
        return cleaned_data
    class Meta:
        model = Challenge
        # fields = "__all__"
        fields = {'title', 'requirment', 'award', 'chtype', 'technology'}