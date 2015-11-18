# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

import logging

from django.core.cache import cache

from monitor.models import RecordQueue

logger = logging.getLogger(__name__)


def add_bracket(text):
    return '【' + text + '】'


def send_message(record, plugin):
    category = plugin.category
    user_set = category.user_set.all()
    if RecordQueue.objects.filter(record=record, plugin=plugin).exists():
        return

    record_queue_list = []
    for user in user_set:
        record_queue = RecordQueue.objects.create(
            record=record,
            plugin=plugin,
            category=category,
            user=user,
            sent=False
        )
        record_queue_list.append(record_queue)

    from monitor.tasks import send_email
    send_email.apply_async(kwargs={
        'mail_sub': '%s%s%s%s' % (
            add_bracket(category.name),
            add_bracket(plugin.name),
            add_bracket(record.postdate) if record.postdate else '',
            record.title,
        ),
        'mail_message': '<h3>原文链接: <a href="%s">%s</a></h3><br/><br/>' % (record.url, record.url) + record.content,
        'to_list': [user.email for user in user_set],
        'record_id_list': [record_queue.pk for record_queue in record_queue_list],
    }, routing_key='email')

    logger.info('Sent message to [%s]: [%s][%s][%s]' % (
        ','.join([user.email for user in user_set]),
        plugin.iden,
        record.title,
        record.url
    ))


def resend_fail_record(record_queue):
    record = record_queue.record
    plugin = record_queue.plugin
    category = record_queue.category
    user = record_queue.user

    from monitor.tasks import send_email
    send_email.apply_async(kwargs={
        'mail_sub': '%s%s%s%s' % (
            add_bracket(category.name),
            add_bracket(plugin.name),
            add_bracket(record.postdate) if record.postdate else '',
            record.title,
        ),
        'mail_message': '<h3>原文链接: <a href="%s">%s</a></h3><br/><br/>' % (record.url, record.url) + record.content,
        'to_list': [user.email],
        'record_id_list': [record_queue.pk],
    }, routing_key='email')


class TaskLock(object):

    key = 'zq_monitor_lock'
    timeout = 3600

    @staticmethod
    def is_duplicate():
        if cache.get(TaskLock.key):
            return True
        else:
            return False

    @staticmethod
    def lock():
        cache.set(TaskLock.key, True, TaskLock.timeout)

    @staticmethod
    def unlock():
        cache.delete(TaskLock.key)
