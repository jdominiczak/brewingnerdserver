# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-06 16:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('brewery', '0041_auto_20170406_1529'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='est_pre_boil_vol',
            field=models.DecimalField(decimal_places=4, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='recipe',
            name='pre_boil_vol',
            field=models.DecimalField(decimal_places=4, max_digits=10, null=True),
        ),
    ]
