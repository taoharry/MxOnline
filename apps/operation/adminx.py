#!/usr/bin/env python
#coding:utf8

__Auther__ = "harry"
__Createtime__ = "2017/8/7 11:06"
__Version__ = 1

import xadmin

from  .models import  UserAsk,CourseComments,UserFavorite,UserMessage,UserCource


class UserAskAdmin(object):
    list_display = ["name","mobile","course_name","add_time"]
    search_fields = ["name","mobile","course_name"]
    list_filter = ["name","mobile","course_name","add_time"]


class CourseCommentsAdmin(object):
    list_display = ["user","course","comments","add_time"]
    search_fields = ["user","course","comments"]
    list_filter = ["user","course","comments","add_time"]



class UserFavoriteAdmin(object):
    list_display = ["user","fav_id","has_read","add_time"]
    search_fields = ["user","fav_id","fav_type"]
    list_filter = ["user","fav_id","fav_type","add_time"]


class UserMessageAdmin(object):
    list_display = ["user","message","url","index","add_time"]
    search_fields = ["user","message","url","index"]
    list_filter = ["user","message","url","index","add_time"]


class UserCourceAdmin(object):
    list_display = ["user","course","add_time"]
    search_fields = ["user","course"]
    list_filter = ["user","course","add_time"]


xadmin.site.register(UserAsk, UserAskAdmin)
xadmin.site.register(CourseComments, CourseCommentsAdmin)
xadmin.site.register(UserFavorite, UserFavoriteAdmin)
xadmin.site.register(UserMessage, UserMessageAdmin)
xadmin.site.register(UserCource, UserCourceAdmin)