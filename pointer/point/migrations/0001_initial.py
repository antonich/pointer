# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-03-02 10:11
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Pointer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, default=b'', max_length=40)),
                ('description', models.CharField(blank=True, default=b'', max_length=100)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('pointer_date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'ordering': ['pointer_date'],
            },
        ),
        migrations.CreateModel(
            name='PrivatePointer',
            fields=[
                ('pointer_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='point.Pointer')),
                ('is_private', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
            ],
            bases=('point.pointer',),
        ),
        migrations.CreateModel(
            name='PublicPointer',
            fields=[
                ('pointer_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='point.Pointer')),
                ('is_private', models.BooleanField(default=False)),
            ],
            bases=('point.pointer',),
        ),
    ]
