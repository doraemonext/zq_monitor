# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

import logging

from monitor.models import RecordQueue
from monitor.tasks import send_email

logger = logging.getLogger(__name__)


def add_bracket(text):
    return '【' + text + '】'


def send_message(record, plugin):
    category = plugin.category
    user_set = category.user_set.all()
    for user in user_set:
        if RecordQueue.objects.filter(record=record, plugin=plugin, user=user).exists():
            continue
        record_queue = RecordQueue.objects.create(
            record=record,
            plugin=plugin,
            category=category,
            user=user,
            sent=False
        )
        send_email.apply_async(kwargs={
            'mail_sub': '%s%s%s%s' % (
                add_bracket(category.name),
                add_bracket(plugin.name),
                add_bracket(record.postdate) if record.postdate else '',
                record.title,
            ),
            'mail_message': '<h3>原文链接: <a href="%s">%s</a></h3><br/><br/>' % (record.url, record.url) + record.content,
            'to_list': [user.email],
            'record_id': record_queue.pk,
        }, routing_key='email')
        logger.info('Sent message: [%s][%s][%s]' % (plugin.iden, record.title, record.url))
