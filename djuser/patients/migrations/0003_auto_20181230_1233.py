# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-12-30 06:48
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('patients', '0002_patient_comment'),
    ]

    operations = [
        migrations.RenameField(
            model_name='patient',
            old_name='comment',
            new_name='desctiption',
        ),
    ]
