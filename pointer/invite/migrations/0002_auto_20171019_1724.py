# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-10-19 17:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invite', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invite',
            name='date',
            field=models.DateTimeField(),
        ),
    ]
