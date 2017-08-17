#coding:utf-8
import json
from django.shortcuts import render
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.views.generic.base import View
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse,HttpResponseRedirect

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from .models import UserProfile,EmailVerityRecord,Banner
from .forms import LoginForm,RegisterForm,ForgetForm,ModifypwdForm,UploadimageForm,UserInfoForm
from utils.email_send import send_register_email
from utils.mixin_until import LoginRequiredMixin
from operation.models import UserProfile,UserFavorite,UserMessage,UserCource
from organization.models import  Teacher,CourseOrg
from courses.models import CourseOrg,Course


# Create your views here.
#改写认证检验方法authenticate
class CustomBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username)|Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return  None


#继承view的基类来直接和wsgi通讯
class RegisterView(View):
    #注册页面
    def get(self,request):
        register_form = RegisterForm()
        return render(request,"register.html",{"register_form":register_form})

    def post(self,request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            email = request.POST.get("email","")
            if UserProfile.objects.filter(email=email):
                return render(request,"register.html",{"register_form":register_form,"msg":"用户已注册"})
            password = request.POST.get("password","")
            user_profile = UserProfile()
            user_profile.username = email
            user_profile.email = email
            user_profile.is_active = False
            user_profile.password = make_password(password)
            user_profile.save()
            send_register_email(email,"register")
            # 写入欢迎注册消息
            user_message = UserMessage()
            user_message.user = user_profile.id
            user_message.message = "欢迎注册慕学在线网"
            user_message.save()

            return  render(request, "login.html")
        else:
            return render(request, "register.html",{"register_form":register_form})

#用户登出
class LogoutView(View):
    def get(self,request):
        logout(request)
        from django.core.urlresolvers import reverse
        return HttpResponseRedirect(reverse('index'))


#用户登入
class LoginView(View):
    def get(self,request):
        return render(request,"login.html",{"msg":"用户名或密码错误"})

    def post(self,request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get("username", "")
            pass_word = request.POST.get("password", "")
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    #如果直接登入不会加载数据
                    #return render(request, "index.html",)
                    from django.core.urlresolvers import reverse
                    return HttpResponseRedirect(reverse('index'))
                else:
                    return render(request, "login.html", {"msg": "用户未激活"})

        else:
            return render(request, "login.html", {"msg": "用户名或密码错误"})


class ActiveView(View):
    def get(self,request,active_code):
        all_records = EmailVerityRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()

        else:
            return render(request,"active_fail.html")

        return render(request,"login.html")


class ForgetPwdView(View):
    def get(self,request):
        forget_form = ForgetForm()
        return render(request,"forgetpwd.html",{"forget_form":forget_form})

    def post(self,request):
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get("email","")
            send_register_email(email,"forget")
            return render(request,"send_email.html")


class ResetView(View):
    def get(self,request,active_code):
        all_records = EmailVerityRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                return render(request,"password_reset.html",{"email":email})


class ModifypwdView(View):
    def post(self,request):
        modifypwd_form = ModifypwdForm(request.POST)
        if modifypwd_form.is_valid():
            pwd1 = request.POST.get("password1","")
            pwd2 = request.POST.get("password2", "")
            email = request.POST.get("email","")
            if pwd1 != pwd2:
                return render(request,"password_reset.html",{"email":email,"msg":"用户密码不一致"})

            user = UserProfile.objects.get(email=email)
            user.password = make_password(pwd1)
            user.save()
            return render(request,"login.html")
        else:
            print "from is error"


class UserinfoView(LoginRequiredMixin,View):
    """
    用户个人信息
    """
    def get(self,request):
        return render(request,"usercenter-info.html",{})

    def post(self,request):
        user_info_form=UserInfoForm(request.POST,instance=request.user)
        if user_info_form.is_valid():
            user_info_form.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(user_info_form.errors), content_type='application/json')


class UserUploadimageView(View):
    """
    个人中心页面重新上传个人图片
    """
    def post(self,request):
        image_form = UploadimageForm(request.POST, request.FILES,instance=request.user)
        if image_form.is_valid():
            image_form.save()
            return  HttpResponse("{'status':'sucess'}",content_type='application/json')
        else:
            return HttpResponse("{'status':'fail','msg':'用户未登录'}", content_type='application/json')


class UserUpdatepwdView(View):
    """
    个人中心页面重新上传密码
    """

    def post(self,request):
        modifypwd_form = ModifypwdForm(request.POST)
        if modifypwd_form.is_valid():
            pwd1 = request.POST.get("password1","")
            pwd2 = request.POST.get("password2", "")
            if pwd1 != pwd2:
                return HttpResponse("{'status':'fail','msg':'密码不一致'}", content_type='application/json')

            user = request.user
            user.password = make_password(pwd1)
            user.save()
            return HttpResponse("{'status':'sucess'}", content_type='application/json')

        else:
            return HttpResponse(json.dump(modifypwd_form.errors), content_type='application/json')


class SendEmailCodeView(LoginRequiredMixin,View):
    #发送邮箱验证码
    def get(self,request):
        email = request.GET.get("email","")
        if UserProfile.objects.filter(email=email):
            return HttpResponse("{'email':'邮箱已经存在'}",content_type='application/json')

        send_register_email(email,"update_email")
        return HttpResponse("{'email':'sucess'}", content_type='application/json')


class UpdateEmailView(LoginRequiredMixin,View):
    def post(self,request):
        email = request.POST.get("email",'')
        code  = request.POST.get("code",'')
        existed_records = EmailVerityRecord.objects.filter(email=email,code=code,send_type='update_email')
        if existed_records:
            user = request.user
            user.email = email
            user.save()
            return HttpResponse('{"email":"修改成功"}', content_type='application/json')
        else:
            return HttpResponse('{"email":"验证码出错"}', content_type='application/json')



class MyCourseView(LoginRequiredMixin,View):
    # 我的课程
    def get(self,request):
        user_courses=UserCource.objects.filter(user=request.user)
        return render(request,"usercenter-mycourse.html",{
            "user_courses":user_courses

        })

class MyFavOrgView(LoginRequiredMixin,View):
    # 我收藏的课程机构
    def get(self,request):
        org_list=[]
        fav_orgs=UserFavorite.objects.filter(user=request.user,fav_type=2)
        for fav_org in fav_orgs:
            org_id=fav_org.fav_id
            org=CourseOrg.objects.get(id=org_id)
            org_list.append(org)

        return render(request,"usercenter-fav-org.html",{
            "org_list":org_list
        })


class MyFavTeacherView(LoginRequiredMixin, View):
    # 我收藏的授课讲师
    def get(self, request):
        teacher_list = []
        print  type(request.user),request.user
        fav_teacher = UserFavorite.objects.filter(user=request.user, fav_type=3)
        for fav_teacher in fav_teacher:
            teacher_id = fav_teacher.fav_id
            teacher = Teacher.objects.get(id=teacher_id)
            teacher_list.append(teacher)

        return render(request, "usercenter-fav-teacher.html", {
            "teacher_list": teacher_list

        })

class MyFavCourseView(LoginRequiredMixin,View):
    # 我收藏的课程
    def get(self,request):
        course_list=[]
        fav_course=UserFavorite.objects.filter(user=request.user,fav_type=1)
        for fav_course in fav_course:
            course_id=fav_course.fav_id
            course=Course.objects.get(id=course_id)
            course_list.append(course)

        return render(request,"usercenter-fav-course.html",{
            "course_list":course_list

        })


class MyMessageView(LoginRequiredMixin,View):
    # 我的消息
    def get(self,request):
        all_message=UserMessage.objects.filter(user=request.user.id)
        # 用户进入个人消息后清空未读消息的记录
        all_unread_messages=UserMessage.objects.filter(user=request.user.id,has_read=False)
        for unread_message in all_unread_messages:
            unread_message.has_read=True
            unread_message.save()

        # 对个人消息进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        # Provide Paginator with the request object for complete querystring generatio
        p = Paginator(all_message, 3, request=request)
        messages = p.page(page)
        return render(request,"usercenter-message.html",{
            "messages":messages

        })



class IndexView(View):
    # 慕学网首页
    def get(self,request):
        # 取出轮播图
        all_banners=Banner.objects.all().order_by('index')
        courses=Course.objects.filter(is_banner=False)[:4]
        banner_courses=Course.objects.filter(is_banner=True)[:3]
        course_orgs=CourseOrg.objects.all()[:15]



        return render(request,"index.html",{
            "all_banners":all_banners,
            "courses":courses,
            "banner_courses":banner_courses,
            "course_orgs":course_orgs


        })


# 全局配置404
def page_not_found(request):
    from django.shortcuts import render_to_response
    response=render_to_response('404.html',{})
    response.status_code=404
    return response


# 全局配置500
def page_errror(request):
    from django.shortcuts import render_to_response
    response=render_to_response('500.html',{})
    response.status_code=500
    return response




'''
def user_login(request):
    if request.method == "POST":
        user_name = request.POST.get("username", "")
        pass_word =  request.POST.get("password", "")
        user = authenticate(username=user_name,password=pass_word)
        if user is not None:
            login(request,user)
            return render(request,"index.html")
        else:
            return render(request,"login.html",{"msg":"用户名或密码错误"})
    elif request.method == "GET":
        return  render(request,"login.html",{})

'''