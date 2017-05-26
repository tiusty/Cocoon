# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-05-25 22:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('houseDatabase', '0006_auto_20170525_1813'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rentdatabase',
            name='lat',
            field=models.DecimalField(decimal_places=6, default=0, max_digits=9),
        ),
        migrations.AlterField(
            model_name='rentdatabase',
            name='lon',
            field=models.DecimalField(decimal_places=6, default=0, max_digits=9),
        ),
    ]
