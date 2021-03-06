# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-13 14:24
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('brewery', '0006_misc'),
    ]

    operations = [
        migrations.CreateModel(
            name='Misc_usage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('time', models.IntegerField()),
                ('amount', models.DecimalField(decimal_places=4, max_digits=10)),
                ('amount_is_weight', models.BooleanField(default=False)),
                ('misc', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='brewery.Misc')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='brewery.Recipe')),
            ],
        ),
        migrations.AddField(
            model_name='recipe',
            name='misc',
            field=models.ManyToManyField(through='brewery.Misc_usage', to='brewery.Misc'),
        ),
    ]
