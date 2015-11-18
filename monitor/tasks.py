# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

import logging
import socket

import requests
from requests.exceptions import RequestException
from django.conf import settings

from monitor.plugins.base import PluginManager
from monitor.plugins.exceptions import PluginException, PluginRequestError
from monitor.models import RecordQueue
from monitor.utils import TaskLock, resend_fail_record
from zq_monitor.celery import app

logger = logging.getLogger(__name__)


@app.task(bind=True)
def send_email(self, mail_sub, mail_message, to_list, record_id_list):
    try:
        r = requests.post(
            url=settings.MAIL_URL,
            auth=("api", settings.MAIL_APIKEY),
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

    for record_id in record_id_list:
        record_queue = RecordQueue.objects.get(pk=record_id)
        record_queue.sent = True
        record_queue.save()


@app.task(bind=True)
def run(self):
    if TaskLock.is_duplicate():
        logger.warning('Duplicate task, abort now')
        return

    TaskLock.lock()
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
        logger.info('Finished plugin %s' % plugin['iden'])

    TaskLock.unlock()
    logger.info('Successfully ran monitor')


@app.task(bind=True)
def maintain_fail_mail(self):
    if TaskLock.is_duplicate():
        logger.warning('Conflict task, abort now')
        return

    TaskLock.lock()
    logger.info('Starting maintain fail mail record...')
    record_queue = RecordQueue.objects.filter(sent=False)
    for item in record_queue:
        resend_fail_record(item)
        logger.info('Resend mail record %s to %s' % (item.record.title, item.user.email))

    TaskLock.unlock()
    logger.info('Finished maintain fail mail record.')