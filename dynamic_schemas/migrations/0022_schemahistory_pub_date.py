# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-18 09:01
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('dynamic_schemas', '0021_auto_20180118_0931'),
    ]

    operations = [
        migrations.AddField(
            model_name='schemahistory',
            name='pub_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
