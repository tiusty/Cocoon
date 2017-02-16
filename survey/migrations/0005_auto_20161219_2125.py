# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-20 02:25
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models
import re


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0004_auto_20161219_2020'),
    ]

    operations = [
        migrations.AlterField(
            model_name='initialsurveymodel',
            name='zip_code',
            field=models.IntegerField(default=-1),
        ),
        migrations.AlterField(
            model_name='rentingsurveymodel',
            name='homeType',
            field=models.CharField(default='0', max_length=200, validators=[django.core.validators.RegexValidator(re.compile('^\\d+(?:\\,\\d+)*\\Z', 32), code='invalid', message='Enter only digits separated by commas.')]),
        ),
        migrations.AlterField(
            model_name='rentingsurveymodel',
            name='name',
            field=models.CharField(default='recent_survey', max_length=200),
        ),
    ]
