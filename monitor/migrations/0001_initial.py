# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MoniterCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64, verbose_name='\u5206\u7c7b\u540d\u79f0')),
            ],
            options={
                'db_table': 'monitor_category',
                'verbose_name': '\u76d1\u89c6\u5206\u7c7b',
                'verbose_name_plural': '\u76d1\u89c6\u5206\u7c7b',
            },
        ),
        migrations.CreateModel(
            name='MoniterUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nickname', models.CharField(max_length=64, verbose_name='\u6635\u79f0')),
                ('email', models.EmailField(max_length=255, verbose_name='\u90ae\u4ef6\u5730\u5740')),
                ('category', models.ManyToManyField(to='monitor.MoniterCategory', verbose_name='\u76d1\u89c6\u5206\u7c7b')),
            ],
            options={
                'db_table': 'monitor_user',
                'verbose_name': '\u76d1\u89c6\u53cd\u9988\u7528\u6237',
                'verbose_name_plural': '\u76d1\u89c6\u53cd\u9988\u7528\u6237',
            },
        ),
    ]
