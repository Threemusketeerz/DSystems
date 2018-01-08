# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-08 14:00
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('dynamic_schemas', '0012_auto_20180104_1431'),
    ]

    operations = [
        migrations.AddField(
            model_name='schema',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='schema',
            name='date_obsolete',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, editable=False),
        ),
    ]
