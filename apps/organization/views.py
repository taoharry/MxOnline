#coding:utf-8

from django.shortcuts import render
from django.views.generic import  View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.db.models import Q

from .models import CityDict,CourseOrg,Teacher
from forms import UserAskForm
from operation.models import UserFavorite
from courses.models import Course
from organization.models import Teacher
# Create your views here.


class OrgView(View):
    """
    课程机构列表功能
    """
    def get(self,request):

        #课程机构
        all_org = CourseOrg.objects.all()
        #城市
        all_city = CityDict.objects.all()
        # 机构搜索
        search_keywords = request.GET.get('sort', '')
        if search_keywords:
            all_org = all_org.filter(
                Q(name__icontains=search_keywords) | Q(desc__icontains=search_keywords))

        # 热门机构排名
        hot_org = all_org.order_by("-click_nums")[0:3]
        #在请求中取出city用作筛选,数据库里面是作为外键存储
        city_id = request.GET.get('city', "")
        if city_id:
            all_org = all_org.filter(city_id=int(city_id))

        # 培训机构类别筛选
        category = request.GET.get("ct", " ")
        if category:
            all_org = all_org.filter(categroy=str(category))

        #按照学习人数排名
        sort = request.GET.get('sort_s', "")
        if city_id:
            if sort=="students":
                all_org = all_org.order_by("-student")
            elif sort=="courses":
                all_org = all_org.order_by("-course_nums")

        org_nums = all_org.count()

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1



        p = Paginator(all_org,2, request=request)

        orgs = p.page(page)

        return render(request, "org-list_back.html", {
            "all_org": orgs,
            "all_city": all_city,
            'org_nums': org_nums,
            "city_id":city_id,
            "category":category,
            "hot_org":hot_org,
            "sort":sort,
        })

class AddUserAskView(View):
    def post(self,request):
        userask_form = UserAskForm(request.POST)
        if userask_form.is_valid():
            #使用了form表单的继承类,就不需要在逐个字段属性赋值后再在数据库里面保存,因为类中已经封装了方法
            user_ask = userask_form.save(commit=True)
            return HttpResponse("{'status':'sucess'}", content_type='application/json')
        else:
            return HttpResponse("{'status':'fail','msg':'信息错误'}")


class OrgHomeView(View):
    """
    机构首页
    """
    def get(self,request, org_id):
        current_page = "home"
        course_org = CourseOrg.objects.get(id=int(org_id))
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user,fav_id=course_org.id,fav_type=2):
                has_fav = True

        #table_set反向查找
        all_courses = course_org.course_set.all()[:3]
        all_teachers = course_org.teacher_set.all()[:1]
        return render(request, 'org-detail-homepage.html',{
            "all_courses":all_courses,
            "all_teachers":all_teachers,
            "course_org":course_org,
            "current_page":current_page,
            "has_fav":has_fav
        })


class OrgCourseView(View):
    """
    机构课程
    """
    def get(self,request, org_id):
        course_org = CourseOrg.objects.get(id=int(org_id))
        #tablename_set反向查找
        all_courses = course_org.course_set.all()
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        current_page = "course"
        return render(request, 'org-detail-course.html',{
            "all_courses":all_courses,
            "course_org":course_org,
            "current_page": current_page,
            "has_fav":has_fav,
        })


class OrgDescView(View):
    """
    机构介绍
    """
    def get(self,request, org_id):
        course_org = CourseOrg.objects.get(id=int(org_id))
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        current_page = "jg"
        return render(request, 'org-detail-desc.html',{

            "course_org":course_org,
            "current_page": current_page,
            "has_fav": has_fav,
        })


class OrgTeacherView(View):
    """
    机构教师页
    """
    def get(self,request, org_id):
        course_org = CourseOrg.objects.get(id=int(org_id))
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        #tablename_set反向查找
        all_teachers = course_org.teacher_set.all()
        current_page = "teacher"
        return render(request, 'org-detail-teachers.html',{
            "all_teachers":all_teachers,
            "course_org":course_org,
            "current_page": current_page,
            "has_fav": has_fav,
        })



class AddFavView(View):
    """
    收藏课程

    """
    def post(self,request):
        fav_id = request.POST.get('fav_id',0)
        fav_type = request.POST.get('fav_type',0)


        if not request.user.is_authenticated():
            return HttpResponse("{'status':'fail','msg':'用户未登录'}",content_type='application/json')

        exist_records = UserFavorite.objects.filter(user=request.user,fav_id=int(fav_id),fav_type=int(fav_type))

        if  exist_records:
            exist_records.delete()
            if exist_records:
                # 如果记录在 表示取消收藏
                exist_records.delete()
                if int(fav_type) == 1:
                    course = Course.objects.get(id=int(fav_id))
                    course.fav_nums -= 1
                    if course.fav_nums < 0:
                        course.fav_nums = 0
                    course.save()
                elif int(fav_type) == 2:
                    course_org = Course.objects.get(id=int(fav_id))
                    course_org.fav_nums -= 1
                    if course_org.fav_nums < 0:
                        course_org.fav_nums = 0
                    course_org.save()
                elif int(fav_type) == 3:
                    teacher = Teacher.objects.get(id=int(fav_id))
                    teacher.fav_nums -= 1
                    if teacher.fav_nums < 0:
                        teacher.fav_nums = 0
                    teacher.save()
            return HttpResponse("{'status':'sucess','msg':'收藏'}", content_type='application/json')
        else:
            user_fav = UserFavorite()
            if fav_id > 0 and fav_type >0:
                user_fav.user = request.user
                user_fav.fav_id = int(fav_id)
                user_fav.fav_type = int(fav_type)
                user_fav.save()

                if int(fav_type) == 1:
                    course = Course.objects.get(id=int(fav_id))
                    course.fav_nums += 1
                    course.save()
                elif int(fav_type) == 2:
                    course_org = Course.objects.get(id=int(fav_id))
                    course_org.fav_nums += 1
                    course_org.save()
                elif int(fav_type) == 3:
                    teacher = Teacher.objects.get(id=int(fav_id))
                    teacher.fav_nums += 1
                    teacher.save()
                return HttpResponse("{'status':'sucess','msg':'已收藏'}", content_type='application/json')
            else:
                return HttpResponse("{'status':'fail','msg':'收藏出错'}",content_type='application/json')


class TeacherView(View):
    """
    讲师列表
    """
    def get(self,request):
        teachers = Teacher.objects.all()

        search_keywords = request.GET.get('sort', '')
        if search_keywords:
            teachers = teachers.filter(
                Q(name__icontains=search_keywords)|Q(work_company__icontains=search_keywords))

        right_sort = Teacher.objects.order_by('-click_nums')[:3]
        hot = request.GET.get('sort','')
        if hot:
            teachers = teachers.order_by('-click_nums')

        all_nums = teachers.count()
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1



        p = Paginator(teachers,2, request=request)

        pg = p.page(page)

        return render(request,"teachers-list.html",{
            "teachers":pg,
            "right_hot":right_sort,
            "all_nums":all_nums,
            "sort":hot
        })


class TeacherDetialView(View):
    def get(self,request,teacher_id):

        teacher = Teacher.objects.get(id=int(teacher_id))

        teacher_sort = Teacher.objects.order_by('-click_nums')[:3]
        teacher_course = Course.objects.filter(teacher=teacher)

        has_teacher_faved=False
        if UserFavorite.objects.filter(user=request.user,fav_type=2,fav_id=teacher.id):
            has_teacher_faved = True
        has_org_faved = False
        if UserFavorite.objects.filter(user=request.user, fav_type=3, fav_id=teacher.id):
            has_org_faved = True


        return render(request, "teacher-detail.html", {
            "teacher_sort":teacher_sort,
            "teacher_course":teacher_course,
            "teacher":teacher,
            "has_teacher_faved":has_teacher_faved,
            "has_org_faved":has_org_faved,

        })