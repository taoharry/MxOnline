#!/usr/bin/env python
#coding:utf8

__Auther__ = "harry"
__Createtime__ = "2017/8/7 17:18"
__Version__ = 1


from django import forms
from captcha.fields import CaptchaField


from .models import UserProfile


class LoginForm(forms.Form):
    #这里的变量需要和html页面中表单提交变量相同
    username = forms.CharField(required=True)
    password = forms.CharField(required=True,min_length=5)


class RegisterForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, min_length=5)
    captcha = CaptchaField(error_messages={"invalid":u"验证码错误"})


class ForgetForm(forms.Form):
    email = forms.EmailField(required=True)
    captcha = CaptchaField(error_messages={"invalid":u"验证码错误"})


class ModifypwdForm(forms.Form):
    password1 = forms.CharField(required=True)
    password2 = forms.CharField(required=True)


class UploadimageForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ["image"]

class UserInfoForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ["nick_name","gender","birday","address","mobile"]

