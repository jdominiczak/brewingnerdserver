# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-13 16:13
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('brewery', '0009_auto_20170313_1611'),
    ]

    operations = [
        migrations.RenameField(
            model_name='yeast',
            old_name='labratory',
            new_name='laboratory',
        ),
    ]
