# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import timedelta.fields


class Migration(migrations.Migration):

    dependencies = [
        ('flex', '0004_auto_20160411_1048'),
    ]

    operations = [
        migrations.AlterField(
            model_name='processchild',
            name='duration',
            field=timedelta.fields.TimedeltaField(null=True, blank=True),
        ),
    ]
