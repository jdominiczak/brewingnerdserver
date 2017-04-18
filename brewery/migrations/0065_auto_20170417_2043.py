# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-17 20:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('brewery', '0064_alert_resolved_timestamp'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='alert',
            name='priority',
        ),
        migrations.AddField(
            model_name='alert',
            name='type',
            field=models.CharField(default='Other', max_length=100),
        ),
    ]