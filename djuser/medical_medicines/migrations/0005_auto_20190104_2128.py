# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2019-01-04 15:43
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('medical_medicines', '0004_auto_20190104_2127'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medicalmedicine',
            name='date',
            field=models.DateField(default=datetime.datetime(2019, 1, 4, 15, 43, 50, 885858, tzinfo=utc)),
        ),
    ]