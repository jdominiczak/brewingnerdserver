# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-13 17:39
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('brewery', '0012_water_water_usage'),
    ]

    operations = [
        migrations.CreateModel(
            name='Equipment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100)),
                ('tun_volume', models.DecimalField(decimal_places=4, max_digits=10)),
                ('tun_weight', models.DecimalField(decimal_places=4, max_digits=10)),
                ('tun_specific_heat', models.DecimalField(decimal_places=4, max_digits=10)),
                ('trub_chiller_loss', models.DecimalField(decimal_places=4, max_digits=10)),
                ('evap_rate', models.DecimalField(decimal_places=4, max_digits=10)),
                ('lauter_deadspace', models.DecimalField(decimal_places=4, max_digits=10)),
                ('hop_utilization', models.DecimalField(decimal_places=4, max_digits=10)),
                ('notes', models.TextField(blank=True)),
                ('default_top_up_kettle', models.DecimalField(decimal_places=4, max_digits=10)),
                ('default_top_up_water', models.DecimalField(decimal_places=4, max_digits=10)),
                ('default_batch_size', models.DecimalField(decimal_places=4, max_digits=10)),
                ('default_boil_size', models.DecimalField(decimal_places=4, max_digits=10)),
            ],
        ),
        migrations.AddField(
            model_name='recipe',
            name='top_up_kettle',
            field=models.DecimalField(decimal_places=4, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='recipe',
            name='top_up_water',
            field=models.DecimalField(decimal_places=4, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='recipe',
            name='equipment',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='brewery.Equipment'),
        ),
    ]
