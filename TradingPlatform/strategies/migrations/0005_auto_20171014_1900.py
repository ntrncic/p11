# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-10-14 19:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('strategies', '0004_auto_20171014_1839'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='slice',
            name='lift_hit',
        ),
        migrations.AddField(
            model_name='slice',
            name='lift_hit_active',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='slice',
            name='lift_hit_delay',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='slice',
            name='lift_hit_offset_num',
            field=models.DecimalField(decimal_places=4, default=1, max_digits=12, verbose_name='Lift Hit Offset from Data point'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='slice',
            name='lift_hit_offset_type',
            field=models.CharField(choices=[('P', '%'), ('C', 'cents')], default=1, max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='slice',
            name='lift_hit_reference_data_point',
            field=models.CharField(choices=[('BEST BID', 'BEST BID'), ('BEST OFFER', 'BEST OFFER'), ('LAST', 'LAST'), ('OPEN', 'OPEN'), ('DAILY HIGH', 'DAILY HIGH'), ('DAILY LOW', 'DAILY LOW'), ('DAILY NET PRICE', 'DAILY NET PRICE'), ('MTD NET PRICE', 'MTD NET PRICE'), ('NUMBER', 'NUMBER')], default=1, max_length=20),
            preserve_default=False,
        ),
    ]
