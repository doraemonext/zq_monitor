# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0005_auto_20151117_0000'),
    ]

    operations = [
        migrations.AddField(
            model_name='recordqueue',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 16, 18, 24, 4, 905376, tzinfo=utc), verbose_name='\u8bb0\u5f55\u65e5\u671f', auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='record',
            name='postdate',
            field=models.CharField(max_length=255, verbose_name='\u53d1\u5e03\u65f6\u95f4'),
        ),
        migrations.AlterField(
            model_name='record',
            name='title',
            field=models.CharField(max_length=255, verbose_name='\u6807\u9898'),
        ),
    ]
