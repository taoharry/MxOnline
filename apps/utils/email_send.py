#!/usr/bin/env python
#coding:utf8

__Auther__ = "harry"
__Createtime__ = "2017/8/8 13:37"
__Version__ = 1

from random import  Random
from django.core.mail import send_mail

from users.models import EmailVerityRecord
from MxOnline.settings import  EMAIL_FROM

def random_str(randomlength=8):
    str=''
    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
    length =len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str +=chars[random.randint(0,length)]

    return str

def send_register_email(email,send_type=0):
    email_record = EmailVerityRecord()
    if send_type == "update_email":
        code = random_str(4)
    else:
        code = random_str(16)
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()

    email_title = ""
    email_body = ""

    if send_type == "register":
        email_title = u"慕学在线网注册激活链接"
        email_body = u"请点击下面的链接激活你的账号: http://127.0.0.1:8000/active/{}".format(code)


        send_status = send_mail(email_title,email_body,EMAIL_FROM,[email,])

        if send_status:
            pass

    elif send_type == "forget":
        email_title = u"慕学在线密码重置链接"
        email_body = u"请点击下面的链接重置你的密码: http://127.0.0.1:8000/reset/{}".format(code)


        send_status = send_mail(email_title,email_body,EMAIL_FROM,[email,])

        if send_status:
            pass

    elif send_type == "update_email":
        email_title = u"慕学邮箱重置"
        email_body = u"验证码 {0}".format(code)


        send_status = send_mail(email_title,email_body,EMAIL_FROM,[email,])

        if send_status:
            pass
