# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-14 20:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('brewery', '0026_recipe_calories'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='boil_time',
            field=models.DecimalField(decimal_places=4, max_digits=10),
        ),
    ]