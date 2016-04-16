# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flex', '0005_auto_20160414_0636'),
    ]

    operations = [
        migrations.AlterField(
            model_name='processchild',
            name='duration',
            field=models.IntegerField(default=0),
        ),
    ]
