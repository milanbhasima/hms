# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2019-01-24 05:03
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('lab_tests', '0020_auto_20190122_1833'),
    ]

    operations = [
        migrations.AlterField(
            model_name='labtest',
            name='date',
            field=models.DateField(default=datetime.datetime(2019, 1, 24, 5, 3, 13, 833011, tzinfo=utc)),
        ),
    ]
