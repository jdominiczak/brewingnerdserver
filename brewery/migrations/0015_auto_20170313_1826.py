# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-13 18:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('brewery', '0014_auto_20170313_1748'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='est_fg',
            field=models.DecimalField(decimal_places=4, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='recipe',
            name='est_ibu',
            field=models.DecimalField(decimal_places=4, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='recipe',
            name='est_og',
            field=models.DecimalField(decimal_places=4, max_digits=10, null=True),
        ),
    ]
