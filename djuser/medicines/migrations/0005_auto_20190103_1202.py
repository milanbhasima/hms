# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2019-01-03 06:17
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('medicines', '0004_auto_20181231_1547'),
    ]

    operations = [
        migrations.RenameField(
            model_name='medicine',
            old_name='doctor',
            new_name='refered_by',
        ),
    ]