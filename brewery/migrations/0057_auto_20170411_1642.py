# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-11 16:42
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('brewery', '0056_recipeassignment'),
    ]

    operations = [
        migrations.CreateModel(
            name='Data',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField()),
                ('data', models.CharField(max_length=200)),
            ],
        ),
        migrations.RenameField(
            model_name='recipe',
            old_name='mash_profile',
            new_name='mash_profile_usage',
        ),
        migrations.AddField(
            model_name='sensor',
            name='unit',
            field=models.CharField(default='Celsius', max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='fermentable_usage',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fermentable_usages', to='brewery.Recipe'),
        ),
        migrations.AlterField(
            model_name='hop_usage',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hop_usages', to='brewery.Recipe'),
        ),
        migrations.AlterField(
            model_name='misc_usage',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='misc_usages', to='brewery.Recipe'),
        ),
        migrations.AlterField(
            model_name='recipeassignment',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assignments', to='brewery.Recipe'),
        ),
        migrations.AlterField(
            model_name='yeast_usage',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='yeast_usages', to='brewery.Recipe'),
        ),
    ]
