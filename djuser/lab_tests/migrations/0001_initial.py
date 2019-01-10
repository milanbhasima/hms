# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-12-31 07:19
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('laboratorists', '0001_initial'),
        ('doctors', '0004_auto_20181228_1325'),
        ('patients', '0004_auto_20181230_1309'),
    ]

    operations = [
        migrations.CreateModel(
            name='LabTest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('test_name', models.CharField(max_length=120)),
                ('test_level', models.CharField(max_length=120)),
                ('test_date', models.DateTimeField(default=datetime.datetime(2018, 12, 31, 7, 19, 8, 973174, tzinfo=utc))),
                ('result', models.TextField()),
                ('follow_up_date', models.DateTimeField(auto_now=True, null=True)),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='patients.Patient')),
                ('refered_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='doctors.Doctor')),
                ('test_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='laboratorists.Laboratorist')),
            ],
        ),
    ]