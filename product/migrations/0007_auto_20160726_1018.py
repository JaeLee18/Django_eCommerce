# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-07-26 10:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0006_auto_20160726_1013'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]