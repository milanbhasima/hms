# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2019-01-16 07:47
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('lab_tests', '0007_auto_20190116_1324'),
    ]

    operations = [
        migrations.AlterField(
            model_name='labtest',
            name='date',
            field=models.DateField(default=datetime.datetime(2019, 1, 16, 7, 47, 48, 143761, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='labtest',
            name='result',
            field=models.CharField(blank=True, default='pending', max_length=120),
        ),
    ]
