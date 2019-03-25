# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2019-01-20 06:43
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('medicines', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='medicine',
            name='supplied_by',
        ),
        migrations.AddField(
            model_name='medicine',
            name='amount',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='medicine',
            name='date',
            field=models.DateField(default=datetime.datetime(2019, 1, 20, 6, 43, 56, 194510, tzinfo=utc)),
        ),
    ]
