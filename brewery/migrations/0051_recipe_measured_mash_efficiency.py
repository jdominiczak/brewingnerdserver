# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-07 18:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('brewery', '0050_auto_20170407_1750'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='measured_mash_efficiency',
            field=models.DecimalField(decimal_places=4, max_digits=10, null=True),
        ),
    ]
