# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-06-01 04:14
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0041_auto_20170601_0011'),
    ]

    operations = [
        migrations.RenameField(
            model_name='rentingsurveymodel',
            old_name='airConditioning',
            new_name='air_conditioning',
        ),
        migrations.RenameField(
            model_name='rentingsurveymodel',
            old_name='dishWasher',
            new_name='dish_washer',
        ),
        migrations.RenameField(
            model_name='rentingsurveymodel',
            old_name='maxBathrooms',
            new_name='max_bathrooms',
        ),
        migrations.RenameField(
            model_name='rentingsurveymodel',
            old_name='minBathrooms',
            new_name='min_bathrooms',
        ),
        migrations.RenameField(
            model_name='rentingsurveymodel',
            old_name='washDryer_InHome',
            new_name='wash_dryer_in_home',
        ),
    ]
