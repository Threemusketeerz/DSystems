# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-18 09:30
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dynamic_schemas', '0022_schemahistory_pub_date'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='SchemaHistory',
            new_name='SchemaHistoryLog',
        ),
    ]
