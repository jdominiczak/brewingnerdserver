# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-04 17:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('brewery', '0035_mash_profile_notes'),
    ]

    operations = [
        migrations.AddField(
            model_name='mash_step',
            name='water_grain_ratio',
            field=models.DecimalField(decimal_places=2, default=1.25, max_digits=10),
            preserve_default=False,
        ),
    ]
