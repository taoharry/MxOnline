#!/usr/bin/env python
#coding:utf8

__Auther__ = "harry"
__Createtime__ = "2017/8/7 10:58"
__Version__ = 1


import  xadmin

from  .models import CityDict,CourseOrg,Teacher


class CityDictAdmin(object):
    list_display = ["name","desc","add_time"]
    search_fields = ["name","desc"]
    list_filter = ["name","desc","add_time"]

class CourseOrgAdmin(object):
    list_display = ["name","desc","click_nums","fav_nums","address","city","add_time"]
    search_fields = ["name","desc","click_nums","fav_nums","address","city"]
    list_filter = ["name","desc","click_nums","fav_nums","address","city","add_time"]

class TeacherAdmin(object):
    list_display = ["org","name","work_years","work_company","work_company","points","click_nums","fav_nums","add_time"]
    search_fields = ["org","name","work_years","work_company","work_company","points","click_nums","fav_nums"]
    list_filter = ["org","name","work_years","work_company","work_company","points","click_nums","fav_nums"]


xadmin.site.register(CityDict, CityDictAdmin)
xadmin.site.register(CourseOrg, CourseOrgAdmin)
xadmin.site.register(Teacher, TeacherAdmin)
