# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-07-26 11:32
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0097_order_cart'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shipping_info',
            name='duration',
            field=models.ForeignKey(blank=True, default=7, null=True, on_delete=django.db.models.deletion.CASCADE, to='order.Shipping_duration'),
        ),
        migrations.AlterField(
            model_name='shipping_info',
            name='iteration',
            field=models.ForeignKey(blank=True, default=2, null=True, on_delete=django.db.models.deletion.CASCADE, to='order.Shipping_iterate'),
        ),
    ]