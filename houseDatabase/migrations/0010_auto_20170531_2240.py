# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-06-01 02:40
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('houseDatabase', '0009_auto_20170531_2239'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rentdatabase',
            name='airConditioning',
        ),
        migrations.RemoveField(
            model_name='rentdatabase',
            name='bath',
        ),
        migrations.RemoveField(
            model_name='rentdatabase',
            name='dishWasher',
        ),
        migrations.RemoveField(
            model_name='rentdatabase',
            name='maxBathrooms',
        ),
        migrations.RemoveField(
            model_name='rentdatabase',
            name='minBathrooms',
        ),
        migrations.RemoveField(
            model_name='rentdatabase',
            name='washDryer_InHome',
        ),
    ]
