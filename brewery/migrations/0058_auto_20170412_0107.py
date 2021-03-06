# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-12 01:07
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('brewery', '0057_auto_20170411_1642'),
    ]

    operations = [
        migrations.AddField(
            model_name='data',
            name='sensor',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='data', to='brewery.Sensor'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='data',
            name='timestamp',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='data',
            name='unit',
            field=models.CharField(default=None, max_length=200),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='data',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='fermenter',
            name='chamber',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fermenter', to='brewery.Chamber'),
        ),
        migrations.AlterField(
            model_name='water_usage',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='water_usages', to='brewery.Recipe'),
        ),
    ]
