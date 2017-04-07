# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-13 19:09
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('brewery', '0016_mash_profile_mash_profile_usage_mash_step_mash_step_usage'),
    ]

    operations = [
        migrations.AddField(
            model_name='mash_step',
            name='mash_order',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='mash_step',
            name='mash_profile',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='brewery.Mash_profile'),
            preserve_default=False,
        ),
        migrations.AlterOrderWithRespectTo(
            name='mash_step',
            order_with_respect_to='mash_order',
        ),
    ]