# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2019-01-29 06:25
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('doctors', '0004_auto_20181228_1325'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='doctor',
            name='joined_date',
        ),
    ]
