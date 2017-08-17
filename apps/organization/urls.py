#!/usr/bin/env python
#coding:utf8

__Auther__ = "harry"
__Createtime__ = "2017/8/11 15:47"
__Version__ = 1
from django.conf.urls import url

from .views import OrgView,AddUserAskView,OrgHomeView,OrgCourseView \
    ,OrgDescView,OrgTeacherView ,AddFavView,TeacherView,TeacherDetialView


urlpatterns =[
    url(r'^list/$', OrgView.as_view(), name="org_list"),
    url(r'^add_ask/$', AddUserAskView.as_view(), name="add_ask"),
    url(r'^home/(?P<org_id>\d+)/$',OrgHomeView.as_view(),name="add_home" ),
    url(r'^course/(?P<org_id>\d+)/$',OrgCourseView.as_view(),name="add_course" ),
    url(r'^desc/(?P<org_id>\d+)/$',OrgDescView.as_view(),name="add_desc" ),
    url(r'^org_teacher/(?P<org_id>\d+)/$',OrgTeacherView.as_view(),name="add_teacher" ),

    #用户机构收藏
    url(r'^add_fav/$',AddFavView.as_view(),name="add_fav" ),

    #讲师列表
    url(r'^teacher/list/$',TeacherView.as_view(),name='teacher_list'),
    #讲师详情页
    url(r'^teacher/detial/(?P<teacher_id>\d+)/$',TeacherDetialView.as_view(),name="teacher_detial" ),
]