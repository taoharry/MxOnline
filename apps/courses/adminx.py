#!/usr/bin/env python
#coding:utf8

__Auther__ = "harry"
__Createtime__ = "2017/8/7 10:31"

import xadmin

from .models import Course,Lesson, Video,CourseResource


class CourseAdmin(object):
    list_display = ["name", "desc", "detail", "degree","learn_time","students","fav_nums","image","add_time"]
    search_fields = ["name", "desc", "detail", "degree","learn_time","students","fav_nums","image"]
    list_filter = ["name", "desc", "detail", "degree","learn_time","students","fav_nums","image","add_time"]


class LessonAdmin(object):
    list_display = ["cource", "name", "add_time"]
    search_fields = ["cource", "name"]
    list_filter = ["cource__name", "name", "add_time"]


class VideoAdmin(object):
    list_display = ["Lesson", "name", "add_time"]
    search_fields = ["Lesson", "name"]
    list_filter = ["Lesson__name", "name", "add_time"]


class CourseResourceAdmin(object):
    list_display = ["cource", "name", "download","add_time"]
    search_fields = ["cource", "name", "download"]
    list_filter = ["cource", "name", "download","add_time"]


xadmin.site.register(Course,CourseAdmin)
xadmin.site.register(Lesson,LessonAdmin)
xadmin.site.register(Video,VideoAdmin)
xadmin.site.register(CourseResource,CourseResourceAdmin)