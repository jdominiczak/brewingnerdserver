# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-06 15:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('brewery', '0040_auto_20170405_1850'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='est_by_mash_efficiency',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='recipe',
            name='est_mash_efficiency',
            field=models.DecimalField(decimal_places=4, max_digits=10, null=True),
        ),
    ]
