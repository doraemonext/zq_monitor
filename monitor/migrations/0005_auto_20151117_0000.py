# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0004_auto_20151116_1819'),
    ]

    operations = [
        migrations.AddField(
            model_name='record',
            name='postdate',
            field=models.CharField(default='', max_length=255, verbose_name='\u53d1\u5e03\u65f6\u95f4'),
        ),
        migrations.AddField(
            model_name='record',
            name='title',
            field=models.CharField(default='', max_length=255, verbose_name='\u6807\u9898'),
        ),
        migrations.AlterField(
            model_name='plugin',
            name='status',
            field=models.BooleanField(default=False, verbose_name='\u542f\u7528\u8be5\u63d2\u4ef6'),
        ),
    ]
