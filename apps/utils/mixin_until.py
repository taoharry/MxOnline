#!/usr/bin/env python
#coding:utf8

__Auther__ = "harry"
__Createtime__ = "2017/8/15 14:43"
__Version__ = 1


from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class LoginRequiredMixin(object):

    @method_decorator(login_required(login_url='/login/'))
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)