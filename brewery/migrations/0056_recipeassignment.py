# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-10 17:10
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('brewery', '0055_mash_profile_usage_sparge_volume'),
    ]

    operations = [
        migrations.CreateModel(
            name='RecipeAssignment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('start_datetime', models.DateTimeField(null=True)),
                ('end_datetime', models.DateTimeField(null=True)),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='device_assignment', to='brewery.Recipe')),
            ],
        ),
    ]
