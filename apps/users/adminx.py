#!/usr/bin/env python
#coding:utf8

import xadmin
from xadmin import views
from xadmin.plugins.auth import UserAdmin

from .models import UserProfile,EmailVerityRecord,Banner



class UserProfileAdmin(UserAdmin):
    pass

class BaseSetting(object):
    #主题功能
    enable_themes = True
    use_bootswatch = True

class GlobalSetting(object):
    #设置页面左上角
    site_title = "慕学后台管理系统"
    #设置页底显示
    site_footer = "慕学在线网"
    #列表缩放
    menu_style = "accordion"


class UserProfileAdmin(object):
    pass


class EmailVerityRecordAdmin(object):
    list_display = ["code","email","send_type","send_time"]
    search_fields = ["code","email","send_type"]
    list_filter = ["code","email","send_type","send_time"]


class BannerAdmin(object):
    list_display = ["title","image","url","index","add_time"]
    search_fields = ["title","image","url","index"]
    list_filter = ["title","image","url","index","add_time"]

from django.contrib.auth.models import User


#注销user
#xadmin.site.unregister(User)
#重新注册用户管理
#xadmin.site.register(UserProfile,UserProfileAdmin)
xadmin.site.register(EmailVerityRecord, EmailVerityRecordAdmin)
xadmin.site.register(Banner, BannerAdmin)
xadmin.site.register(views.BaseAdminView,BaseSetting)
xadmin.site.register(views.CommAdminView,GlobalSetting)

