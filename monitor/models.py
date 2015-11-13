# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

from django.db import models


class MoniterCategory(models.Model):
    name = models.CharField('分类名称', max_length=64)

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'monitor_category'
        verbose_name = '监视分类'
        verbose_name_plural = '监视分类'


class MoniterUser(models.Model):
    nickname = models.CharField('昵称', max_length=64)
    email = models.EmailField('邮件地址', max_length=255)
    category = models.ManyToManyField(MoniterCategory, verbose_name='监视分类')

    def __unicode__(self):
        return self.nickname + ' ' + self.email

    class Meta:
        db_table = 'monitor_user'
        verbose_name = '监视反馈用户'
        verbose_name_plural = '监视反馈用户'

