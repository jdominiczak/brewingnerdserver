# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-10 20:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('brewery', '0003_remove_recipe_creator'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='modified_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
