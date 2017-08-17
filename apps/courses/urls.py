#!/usr/bin/env python
#coding:utf8

__Auther__ = "harry"
__Createtime__ = "2017/8/14 13:35"
__Version__ = 1

from django.conf.urls import url


from .views import CourseListView,CourseDetialView,CourseInfoView,CourseCommentView, \
    AddComentsView, CoursePlayView

urlpatterns =[
    url(r'^list/$', CourseListView.as_view(), name="course_list"),
    #课程详情页
    url(r'^detial/(?P<course_id>\d+)/$', CourseDetialView.as_view(), name="course_detial"),
    # 课程详情页
    url(r'^info/(?P<course_id>\d+)/$', CourseInfoView.as_view(), name="course_info"),
    # 课程评论
    url(r'^comment/(?P<course_id>\d+)/$',CourseCommentView.as_view(), name="course_comments"),
    # 添加课程评论
    url(r'^add_comment/$', AddComentsView.as_view(), name="add_comment"),
    #视频播放
    url(r'^video/(?P<vedieo_id>\d+)/$', CoursePlayView.as_view(), name="vedio_play"),
]