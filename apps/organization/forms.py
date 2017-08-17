#!/usr/bin/env python
#coding:utf8

__Auther__ = "harry"
__Createtime__ = "2017/8/11 14:37"
__Version__ = 1

from django import forms
import re

from operation.models import UserAsk


class UserAskForm(forms.ModelForm):
    """
    modelfrom 可以直接使用model的类中字段定义form,原理上就是根据
    在字段在数据库里面限制,转化为form里面字段限制
    """

    class Meta:
        model = UserAsk
        fields = ["name", "mobile", "course_name"]

    def clean_mobile(self):
        """
        做字段的校验必须这么写

        """

        mobile = self.cleaned_data['mobile']
        REGEX_MOBILE = "^1[358]\d{9}|^147\d{8}|^176\d{8}"
        p = re.compile(REGEX_MOBILE)
        if p.match(mobile):
            return mobile
        else:
            raise forms.ValidationError(u"手机号码非法",code="model_invilad")