#coding:utf-8
from __future__ import unicode_literals
from datetime import datetime

from django.db import models
from organization.models import CourseOrg,Teacher


# Create your models here.



class Course(models.Model):
    courseorg = models.ForeignKey(CourseOrg, verbose_name=u'课程机构',null=True,blank=True)
    teacher = models.ForeignKey(Teacher, verbose_name=u'讲师', null=True, blank=True)
    name = models.CharField(max_length=50 ,verbose_name=u"课程名")
    desc = models.CharField(max_length=300, verbose_name=u"课程描述")
    detail = models.TextField(verbose_name=u"课程详情")
    degree = models.CharField(choices=(("cj",u"初级"),("zj",u"中级"),("gj",u"高级")), max_length=2)
    learn_time = models.IntegerField(default=0, verbose_name=u"学习时长(分)")
    students = models.IntegerField(default=0, verbose_name=u"学习人数")
    fav_nums = models.IntegerField(default=0, verbose_name=u"收藏人数")
    catgary = models.CharField(max_length=20, verbose_name=u"课程类别",default="web开发/后端开发")
    image = models.ImageField(upload_to="courses/%Y/%m", verbose_name=u"封面图片")
    click_nums = models.IntegerField(default=0, verbose_name=u"点击数")
    tag = models.CharField(default='',verbose_name=u"课程标签",max_length=20)
    add_time = models.DateTimeField(default=datetime.now,    verbose_name = u"添加时间")
    youneed_know = models.CharField(max_length=50 ,verbose_name=u"你需要知道什么",default='')
    teacher_tell = models.CharField(max_length=50 ,verbose_name=u"老师告诉你",default='')
    #增加字段是否是轮播图
    is_banner = models.BooleanField(default=False,verbose_name=u'轮播图')


    class Meta:
        verbose_name = u"课程"
        verbose_name_plural = verbose_name

    def get_col_nu(self):
        """
        数据库外键关联反向查询章节数量

        """
        return self.lesson_set.all().count()

    def get_learn_user(self):
        return self.usercource_set.all()[:5]

    def get_all_lesson(self):
        """
        数据库所有章节

        """
        return self.lesson_set.all()

    def __unicode__(self):
        return self.name


class Lesson(models.Model):
    cource = models.ForeignKey(Course, verbose_name=u"课程")
    name = models.CharField(max_length=100, verbose_name=u"章节名")
    learn_time = models.IntegerField(default=0, verbose_name=u"学习时长(分)")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"章节"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return  self.name

    def get_lesson_video(self):
        #获取章节课程
        return self.video_set.all()



class Video(models.Model):
    Lesson = models.ForeignKey(Lesson, verbose_name=u"章节")
    name = models.CharField(max_length=100, verbose_name=u"视频名")
    url = models.CharField(max_length=200,default='', verbose_name=u"url地址")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"视频"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name

class CourseResource(models.Model):
    cource = models.ForeignKey(Course, verbose_name=u"课程")
    name = models.CharField(max_length=100, verbose_name=u"名称")
    download = models.FileField(upload_to="cource/resource/%Y/%m", verbose_name=u"资源文件", max_length=100)
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"课程资源"
        verbose_name_plural = verbose_name