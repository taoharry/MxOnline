# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-08-15 10:29
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0007_lesson_learn_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='courseorg',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='organization.Teacher', verbose_name='\u8bb2\u5e08'),
        ),
    ]