# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2019-01-20 06:39
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('lab_tests', '0009_auto_20190120_1222'),
    ]

    operations = [
        migrations.AlterField(
            model_name='labtest',
            name='date',
            field=models.DateField(default=datetime.datetime(2019, 1, 20, 6, 39, 34, 475363, tzinfo=utc)),
        ),
    ]
