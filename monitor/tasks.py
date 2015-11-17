# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

import logging
import socket

import requests
from requests.exceptions import RequestException

from monitor.plugins.base import PluginManager
from monitor.plugins.exceptions import PluginException, PluginRequestError

from monitor.models import RecordQueue
from zq_monitor.celery import app

logger = logging.getLogger(__name__)


@app.task(bind=True)
def send_email(self, mail_sub, mail_message, to_list, record_id):
    try:
        r = requests.post(
            url="https://api.mailgun.net/v3/mail.doraemonext.com/messages",
            auth=("api", "key-c035c61e9760229b7c5620068a836532"),
            data={
                "from": u"自强信使 <messenger@mail.doraemonext.com>",
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
