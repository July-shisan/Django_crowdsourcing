#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from django import forms
from .models import User, Challenge, Developer, SolutionFile
from .PreTec.eval import pre_technology
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
        # fields = {'p_name', 'password', 'email'}
        # fields = "__all__"
        fields = {'username', 'password', 'email'}

class deveregisterForm(forms.ModelForm):
    password_confirmation = forms.CharField()
    email = forms.EmailField(required=False)
    def clean(self):
        cleaned_data = super(deveregisterForm, self).clean()
        password = cleaned_data.get('password')
        password_confirmation = cleaned_data.get('password_confirmation')
        if password != password_confirmation:
            raise forms.ValidationError(message="两次密码输入不一致")
        return cleaned_data
    class Meta:
        model = Developer
        fields = {'devename', 'password', 'email'}

class develoginForm(forms.ModelForm):
    class Meta:
        model = Developer
        fields = {'devename', 'password'}

class loginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = {'username', 'password'}
        # fields = {'username', 'password'}

class challengeForm(forms.ModelForm):
    technology = forms.CharField(required=False)
    def clean(self):
        cleaned_data = super(challengeForm, self).clean()
        title = cleaned_data.get('title')
        req = cleaned_data.get('requirment')
        if cleaned_data.get('technology') == '':
            if title is not None and req is not None:
                pre_tec = pre_technology(title, req)
                tec = ''
                for i in pre_tec:
                    tec += i
                    tec += ' '
                cleaned_data['technology'] = tec.strip()
        return cleaned_data
    class Meta:
        model = Challenge
        # fields = "__all__"
        fields = {'title', 'requirment', 'award', 'chtype', 'technology'}

class uploadForm(forms.ModelForm):
    class Meta:
        model = SolutionFile
        fields = {'file'}