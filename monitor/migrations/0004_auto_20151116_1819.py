# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0003_plugin_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='plugin',
            name='status',
            field=models.BooleanField(default=False, verbose_name='\u662f\u5426\u542f\u7528'),
        ),
        migrations.AlterField(
            model_name='plugin',
            name='iden',
            field=models.CharField(max_length=255, verbose_name='\u6807\u8bc6\u7b26(\u63d2\u4ef6\u76ee\u5f55)'),
        ),
    ]
