# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flex', '0002_process_process_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProcessChild',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('process_id', models.CharField(max_length=20)),
                ('name', models.CharField(max_length=200)),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('status', models.BooleanField(default=False)),
                ('duration', models.BooleanField(default=False)),
            ],
        ),
        migrations.RemoveField(
            model_name='process',
            name='end_time',
        ),
        migrations.RemoveField(
            model_name='process',
            name='exceeded',
        ),
        migrations.RemoveField(
            model_name='process',
            name='process_id',
        ),
        migrations.RemoveField(
            model_name='process',
            name='start_time',
        ),
        migrations.RemoveField(
            model_name='process',
            name='status',
        ),
    ]
