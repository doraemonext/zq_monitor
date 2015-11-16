# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

import logging
import socket

import requests
from requests.exceptions import RequestException

from monitor.plugins.base import PluginManager
from monitor.models import Plugin
from monitor.plugins.exceptions import PluginException, PluginRequestError

from monitor.models import Record, RecordQueue
from zq_monitor.celery import app

logger = logging.getLogger(__name__)


@app.task(bind=True)
def send_email(self, mail_sub, mail_message, to_list, record_id):
    try:
        r = requests.post(
            url="https://api.mailgun.net/v3/sandboxb76ec3927a684f8194c2083ff587de40.mailgun.org/messages",
            auth=("api", "key-c035c61e9760229b7c5620068a836532"),
            data={
                "from": u"自强信使 <mailgun@sandboxb76ec3927a684f8194c2083ff587de40.mailgun.org>",
                "to": to_list,
                "subject": mail_sub,
                "html": mail_message
            }
        )
    except RequestException, socket.timeout:
        logger.error(u'Timeout: cannot send email message with subject "%s"' % mail_sub)
        return

    if r.status_code != requests.codes.ok:
        logger.error(u'Error %s: cannot send email message with subject "%s"' % (r.text, mail_sub))
    logger.info(u'Successfully sent message: %s' % mail_sub)

    record_queue = RecordQueue.objects.get(pk=record_id)
    record_queue.sent = True
    record_queue.save()


@app.task(bind=True)
def send_message(self, record, plugin):
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
            'mail_sub': u'【%s】【%s】%s' % (category.name, record.postdate, record.title),
            'mail_message': '<h3>原文链接: <a href="%s">%s</a></h3><br/><br/>' % (record.url, record.url) + record.content,
            'to_list': [user.email],
            'record_id': record_queue.pk,
        }, routing_key='email')


@app.task(bind=True)
def run(self):
    manager = PluginManager()
    manager.load_plugins()
    for plugin in manager.plugins:
        plugin_instance = plugin['class'](iden=plugin['iden'], dir=plugin['dir'])
        try:
            plugin_instance.process()
        except PluginRequestError:
            logger.warning('Cannot access plugin %s main url' % plugin['iden'])
        except PluginException:
            logger.exception(u'Error when process plugin %s' % plugin['iden'])
    logger.info('Successfully ran monitor')
