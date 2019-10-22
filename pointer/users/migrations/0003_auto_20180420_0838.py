# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-04-20 08:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_user_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(default='media/default_avatar.png', upload_to='media/avatars'),
        ),
        migrations.AlterField(
            model_name='user',
            name='description',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='user',
            name='name',
            field=models.CharField(blank=True, default='', max_length=130),
        ),
    ]