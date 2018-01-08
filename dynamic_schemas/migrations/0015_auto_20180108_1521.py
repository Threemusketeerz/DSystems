# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-08 14:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dynamic_schemas', '0014_auto_20180108_1513'),
    ]

    operations = [
        migrations.AddField(
            model_name='schema',
            name='date_modified',
            field=models.DateTimeField(auto_now=True, verbose_name='Sidst modificeret'),
        ),
        migrations.AlterField(
            model_name='schema',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Lavet den'),
        ),
        migrations.AlterField(
            model_name='schema',
            name='date_obsolete',
            field=models.DateTimeField(blank=True, editable=False, null=True, verbose_name='Udgået den'),
        ),
    ]
