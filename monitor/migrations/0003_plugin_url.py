# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0002_auto_20151113_1520'),
    ]

    operations = [
        migrations.AddField(
            model_name='plugin',
            name='url',
            field=models.CharField(default='', max_length=255, verbose_name='\u6293\u53d6URL'),
            preserve_default=False,
        ),
    ]
