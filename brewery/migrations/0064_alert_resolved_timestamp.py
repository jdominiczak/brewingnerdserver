# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-17 20:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('brewery', '0063_auto_20170417_1954'),
    ]

    operations = [
        migrations.AddField(
            model_name='alert',
            name='resolved_timestamp',
            field=models.DateTimeField(default=None, null=True),
        ),
    ]