# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-04 14:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('brewery', '0034_auto_20170320_1434'),
    ]

    operations = [
        migrations.AddField(
            model_name='mash_profile',
            name='notes',
            field=models.TextField(blank=True),
        ),
    ]
