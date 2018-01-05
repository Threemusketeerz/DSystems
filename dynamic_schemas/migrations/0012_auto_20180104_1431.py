# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-04 13:31
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dynamic_schemas', '0011_schemaresponse_instruction'),
    ]

    operations = [
        migrations.CreateModel(
            name='SchemaColumn',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=100)),
                ('is_bool', models.BooleanField(default=False, verbose_name='Ja/Nej spørgsmål')),
                ('is_editable', models.BooleanField(default=False, verbose_name='Felt kan ændres')),
                ('schema', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dynamic_schemas.Schema')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='schemaquestion',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='schemaquestion',
            name='schema',
        ),
        migrations.RenameField(
            model_name='schemahelpurl',
            old_name='link_name',
            new_name='name',
        ),
        migrations.DeleteModel(
            name='SchemaQuestion',
        ),
        migrations.AlterUniqueTogether(
            name='schemacolumn',
            unique_together=set([('schema', 'text')]),
        ),
    ]