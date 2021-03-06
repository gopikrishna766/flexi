# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-03-15 11:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Process',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('status', models.BooleanField(default=False)),
                ('exceeded', models.BooleanField(default=False)),
            ],
        ),
    ]
