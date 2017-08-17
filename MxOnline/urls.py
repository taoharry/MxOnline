#coding:utf-8


"""MxOnline URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url,include
from django.contrib import admin
from django.views.generic import TemplateView
#django处理静态文件
from django.views.static import serve
import xadmin




from users.views import LoginView,RegisterView,ActiveView,ForgetPwdView,\
    ResetView,ModifypwdView,LogoutView,IndexView
from organization.views import OrgView
from MxOnline.settings import MEDIA_ROOT



urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    url(r'^captcha/',include('captcha.urls')),

    #用户静态文件加载
    #url("^$",TemplateView.as_view(template_name="index.html"), name="index"),
    url("^$",IndexView.as_view(), name="index"),
    url("^login/$",LoginView.as_view(), name="login"),
    url("^logout/$",LogoutView.as_view(), name="logout"),
    url("^register/$",RegisterView.as_view(), name="register"),
    url("^active/(?P<active_code>.*)/$",ActiveView.as_view(), name="active"),
    url("^forget/$",ForgetPwdView.as_view(), name="forget_pwd"),
    url("^reset/(?P<active_code>.*)/$",ResetView.as_view(), name="reset"),
    url("^modifypwd/$",ModifypwdView.as_view(), name="modify_pwd"),

    #机构跳转到org app下
    url(r'^org/', include("organization.urls",namespace='org')),
    #url(r'^list/$', OrgView.as_view(), name="org_list"),

    #机构跳转到org app下
    url(r'^course/', include("courses.urls",namespace='course')),

    #处理媒体文件访问处理函数
    url(r'^media/(?P<path>.*)$', serve,{"document_root":MEDIA_ROOT}),

    #处理加载静态文件
    #url(r'^static/(?P<path>.*)$', serve,{"document_root":STATIC_ROOT}),

    #用户跳转到用户个人设置下
    url(r'^user/', include("users.urls",namespace='user')),
]

#全局404 500 页面配置,写法固定
# (放ViewS的路径)
handler404='users.views.page_not_found'
handler500='users.views.page_error'