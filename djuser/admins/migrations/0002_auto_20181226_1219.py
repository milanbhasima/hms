# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-12-26 06:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admins', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='admin',
            name='image',
            field=models.FileField(blank=True, null=True, upload_to='profile'),
        ),
    ]