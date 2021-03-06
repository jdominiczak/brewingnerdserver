# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-13 18:44
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('brewery', '0015_auto_20170313_1826'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mash_profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100)),
                ('sparge_temp', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('ph', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Mash_profile_usage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('grain_temp', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('tun_temp', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('equip_adjust', models.BooleanField(default=False)),
                ('mash_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='brewery.Mash_profile')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mash_profile', to='brewery.Recipe')),
            ],
        ),
        migrations.CreateModel(
            name='Mash_step',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100)),
                ('type', models.CharField(max_length=100)),
                ('step_temp', models.DecimalField(decimal_places=2, max_digits=10)),
                ('step_time', models.DecimalField(decimal_places=2, max_digits=10)),
                ('ramp_time', models.IntegerField(default=0)),
                ('end_temp', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Mash_step_usage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('infuse_amount', models.DecimalField(decimal_places=4, max_digits=10, null=True)),
                ('infuse_temp', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('mash_profile_usage', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mash_steps', to='brewery.Mash_profile_usage')),
                ('mash_step', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='brewery.Mash_step')),
            ],
        ),
    ]
