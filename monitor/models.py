# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

import logging

from django.db import models
from django.db.utils import IntegrityError

logger = logging.getLogger(__name__)


class Category(models.Model):
    name = models.CharField('分类名称', max_length=64)

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'monitor_category'
        verbose_name = '监视分类'
        verbose_name_plural = '监视分类'


class User(models.Model):
    nickname = models.CharField('昵称', max_length=64)
    email = models.EmailField('邮件地址', max_length=255)
    category = models.ManyToManyField(Category, verbose_name='监视分类')

    def __unicode__(self):
        return self.nickname + ' ' + self.email

    class Meta:
        db_table = 'monitor_user'
        verbose_name = '监视反馈用户'
        verbose_name_plural = '监视反馈用户'


class Plugin(models.Model):
    category = models.ForeignKey(Category, verbose_name='插件分类')
    name = models.CharField('插件名称', max_length=64)
    iden = models.CharField('标识符(插件目录)', max_length=255)
    url = models.CharField('抓取URL', max_length=255)
    status = models.BooleanField('启用该插件', default=False)

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'monitor_plugin'
        verbose_name = '插件'
        verbose_name_plural = '插件'


class RecordManager(models.Manager):
    def add_record(self, url, content):
        try:
            self.create(url=url, content=content)
            logger.info('Inserted record: %s' % url)
        except IntegrityError:
            logger.info('Repeated record: %s' % url)
            pass


class Record(models.Model):
    url = models.CharField('URL', max_length=255, unique=True, db_index=True)
    content = models.TextField('网页内容')
    timestamp = models.DateTimeField('记录日期', auto_now_add=True)

    objects = RecordManager()

    def __unicode__(self):
        return self.url

    class Meta:
        db_table = 'monitor_record'
        verbose_name = '抓取记录'
        verbose_name_plural = '抓取记录'


class RecordQueue(models.Model):
    record = models.ForeignKey(Record, verbose_name='所属记录')
    plugin = models.ForeignKey(Plugin, verbose_name='所属插件')
    category = models.ForeignKey(Category, verbose_name='所属分类')
    user = models.ForeignKey(User, verbose_name='所属用户')
    sent = models.BooleanField('发送状态', default=False)

    def __unicode__(self):
        return self.record.url + ' ' + self.user.email

    class Meta:
        db_table = 'monitor_record_queue'
        verbose_name = '抓取记录发送队列'
        verbose_name_plural = '抓取记录发送队列'
