# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-13 19:45
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('brewery', '0017_auto_20170313_1909'),
    ]

    operations = [
        migrations.CreateModel(
            name='Fermentation_profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100)),
                ('notes', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Fermentation_step',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100)),
                ('order', models.IntegerField()),
                ('start_temp', models.DecimalField(decimal_places=2, max_digits=10)),
                ('end_temp', models.DecimalField(decimal_places=2, max_digits=10)),
                ('length', models.IntegerField()),
                ('fermentation_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fermentation_steps', to='brewery.Fermentation_profile')),
            ],
        ),
        migrations.AlterField(
            model_name='mash_step',
            name='mash_profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mash_steps', to='brewery.Mash_profile'),
        ),
        migrations.AlterUniqueTogether(
            name='mash_step',
            unique_together=set([('mash_order', 'mash_profile')]),
        ),
        migrations.AddField(
            model_name='recipe',
            name='fermentation_profile',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='brewery.Fermentation_profile'),
        ),
        migrations.AlterUniqueTogether(
            name='fermentation_step',
            unique_together=set([('fermentation_profile', 'order')]),
        ),
    ]
