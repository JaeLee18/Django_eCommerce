# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-07-20 11:28
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0053_auto_20160720_1128'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='start',
            field=models.DateField(blank=True, default=datetime.datetime(2016, 7, 20, 11, 28, 25, 141862), null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='uid',
            field=models.CharField(default='L7VWPQH0WKJZOWKB', max_length=16, null=True),
        ),
    ]