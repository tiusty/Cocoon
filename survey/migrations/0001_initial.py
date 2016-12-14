# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-10 18:47
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('userAuth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='InitialSurvey',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('survey_type', models.BooleanField()),
                ('streetAddress', models.CharField(max_length=200)),
                ('city', models.CharField(max_length=200)),
                ('state', models.CharField(max_length=200)),
                ('zip_code', models.CharField(max_length=200)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='userAuth.UserProfile')),
            ],
        ),
    ]
