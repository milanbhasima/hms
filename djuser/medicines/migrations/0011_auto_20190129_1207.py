# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2019-01-29 06:22
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('medicines', '0010_auto_20190124_1123'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medicine',
            name='date',
            field=models.DateField(default=datetime.datetime(2019, 1, 29, 6, 22, 35, 301161, tzinfo=utc)),
        ),
    ]
