# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-07 14:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('brewery', '0044_auto_20170407_1243'),
    ]

    operations = [
        migrations.AlterField(
            model_name='yeast',
            name='attenuation',
            field=models.DecimalField(decimal_places=4, max_digits=10, null=True),
        ),
    ]