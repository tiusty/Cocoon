# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-05-06 17:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0039_remove_rentingsurveymodel_test'),
    ]

    operations = [
        migrations.AddField(
            model_name='rentingsurveymodel',
            name='price_weight',
            field=models.IntegerField(default=0),
        ),
    ]
