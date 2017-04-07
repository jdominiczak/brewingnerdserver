# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-07 17:50
from __future__ import unicode_literals

from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('brewery', '0049_auto_20170407_1747'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='age',
            field=models.DecimalField(decimal_places=4, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='est_efficiency',
            field=models.DecimalField(decimal_places=4, default=Decimal('72'), max_digits=10),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='name',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
