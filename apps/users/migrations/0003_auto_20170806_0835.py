# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-08-06 08:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20170806_0833'),
    ]

    operations = [
        migrations.AlterField(
            model_name='banner',
            name='index',
            field=models.IntegerField(default=100, verbose_name='\u987a\u5e8f'),
        ),
    ]