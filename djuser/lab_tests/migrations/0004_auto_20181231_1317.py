# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-12-31 07:32
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('lab_tests', '0003_auto_20181231_1304'),
    ]

    operations = [
        migrations.AlterField(
            model_name='labtest',
            name='follow_up_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='labtest',
            name='test_date',
            field=models.DateTimeField(default=datetime.datetime(2018, 12, 31, 7, 32, 7, 753707, tzinfo=utc)),
        ),
    ]
