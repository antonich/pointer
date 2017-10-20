# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-10-19 17:23
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0004_auto_20171019_1700'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='pointer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='event_for_member', to='point.Pointer'),
        ),
    ]
