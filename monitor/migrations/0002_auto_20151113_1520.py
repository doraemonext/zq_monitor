# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Plugin',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64, verbose_name='\u63d2\u4ef6\u540d\u79f0')),
                ('iden', models.CharField(max_length=255, verbose_name='\u6807\u8bc6\u7b26(\u63d2\u4ef6\u6587\u4ef6\u540d)')),
            ],
            options={
                'db_table': 'monitor_plugin',
                'verbose_name': '\u63d2\u4ef6',
                'verbose_name_plural': '\u63d2\u4ef6',
            },
        ),
        migrations.CreateModel(
            name='Record',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.CharField(unique=True, max_length=255, verbose_name='URL', db_index=True)),
                ('content', models.TextField(verbose_name='\u7f51\u9875\u5185\u5bb9')),
                ('timestamp', models.DateTimeField(auto_now_add=True, verbose_name='\u8bb0\u5f55\u65e5\u671f')),
            ],
            options={
                'db_table': 'monitor_record',
                'verbose_name': '\u6293\u53d6\u8bb0\u5f55',
                'verbose_name_plural': '\u6293\u53d6\u8bb0\u5f55',
            },
        ),
        migrations.CreateModel(
            name='RecordQueue',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sent', models.BooleanField(default=False, verbose_name='\u53d1\u9001\u72b6\u6001')),
            ],
            options={
                'db_table': 'monitor_record_queue',
                'verbose_name': '\u6293\u53d6\u8bb0\u5f55\u53d1\u9001\u961f\u5217',
                'verbose_name_plural': '\u6293\u53d6\u8bb0\u5f55\u53d1\u9001\u961f\u5217',
            },
        ),
        migrations.RenameModel(
            old_name='MoniterCategory',
            new_name='Category',
        ),
        migrations.RenameModel(
            old_name='MoniterUser',
            new_name='User',
        ),
        migrations.AddField(
            model_name='recordqueue',
            name='category',
            field=models.ForeignKey(verbose_name='\u6240\u5c5e\u5206\u7c7b', to='monitor.Category'),
        ),
        migrations.AddField(
            model_name='recordqueue',
            name='plugin',
            field=models.ForeignKey(verbose_name='\u6240\u5c5e\u63d2\u4ef6', to='monitor.Plugin'),
        ),
        migrations.AddField(
            model_name='recordqueue',
            name='record',
            field=models.ForeignKey(verbose_name='\u6240\u5c5e\u8bb0\u5f55', to='monitor.Record'),
        ),
        migrations.AddField(
            model_name='recordqueue',
            name='user',
            field=models.ForeignKey(verbose_name='\u6240\u5c5e\u7528\u6237', to='monitor.User'),
        ),
        migrations.AddField(
            model_name='plugin',
            name='category',
            field=models.ForeignKey(verbose_name='\u63d2\u4ef6\u5206\u7c7b', to='monitor.Category'),
        ),
    ]
