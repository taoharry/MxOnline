#!/usr/bin/env python
#coding:utf8

__Auther__ = "harry"
__Createtime__ = "2017/8/16 11:36"
__Version__ = 1


from django.conf.urls import url

from .views import UserinfoView,UserUploadimageView,UserUpdatepwdView,\
    SendEmailCodeView,UpdateEmailView,MyCourseView,MyFavOrgView,MyFavTeacherView, \
    MyFavCourseView,MyMessageView



urlpatterns = [
    #用户信息
    url(r"list/$",UserinfoView.as_view(),name='user_info'),
    # 上传信息
    url(r"upload/file/$", UserUploadimageView.as_view(), name='user_upload'),
    # 修改密码
    url(r"upload/pwd/$", UserUpdatepwdView.as_view(), name='user_upload_pwd'),
    #发送邮箱验证码
    url(r'^sendemail_code/$', SendEmailCodeView.as_view(), name="sendemail_code"),
    # 修改邮箱
    url(r'^update_email/$', UpdateEmailView.as_view(), name="update_email"),
    # 我的课程
    url(r'^mycourse/$', MyCourseView.as_view(), name="mycourse"),
    # 我收藏的课程机构
    url(r'^myfav/org/$', MyFavOrgView.as_view(), name="myfav_org"),
    # 我收藏的授课讲师
    url(r'^myfav/teacher/$', MyFavTeacherView.as_view(), name="myfav_teacher"),
    # 我收藏的课程
    url(r'^myfav/course/$', MyFavCourseView.as_view(), name= "myfav_course"),
    # 我的消息
    url(r'^mymessage/$', MyMessageView.as_view(), name="mymessage"),
]