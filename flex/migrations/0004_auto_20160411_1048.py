# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flex', '0003_auto_20160411_0937'),
    ]

    operations = [
        migrations.AlterField(
            model_name='processchild',
            name='duration',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='processchild',
            name='end_time',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='processchild',
            name='name',
            field=models.ForeignKey(to='flex.Process'),
        ),
    ]
