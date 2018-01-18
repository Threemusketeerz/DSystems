# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-17 15:10
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('dynamic_schemas', '0019_auto_20180117_0959'),
    ]

    operations = [
        migrations.CreateModel(
            name='SchemaHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('new_schema', models.ManyToManyField(related_name='new', to='dynamic_schemas.Schema')),
                ('obsolete_schema', models.ManyToManyField(related_name='obsolete', to='dynamic_schemas.Schema')),
            ],
            managers=[
                ('history', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterField(
            model_name='schemacolumn',
            name='is_editable_once',
            field=models.BooleanField(default=False, verbose_name='Felt kan ændres, en enkelt gang'),
        ),
    ]
