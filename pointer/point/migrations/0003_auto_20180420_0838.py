# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-04-20 08:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('point', '0002_pointer_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pointer',
            name='description',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='pointer',
            name='title',
            field=models.CharField(blank=True, default='', max_length=40),
        ),
    ]
