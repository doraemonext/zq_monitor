# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

import logging
import socket

import requests
from requests.exceptions import RequestException

from monitor.plugins.base import PluginManager
from monitor.models import Plugin
from monitor.plugins.exceptions import PluginException

from zq_monitor.celery import app

logger = logging.getLogger(__name__)


@app.task(bind=True)
def send_message(self, mail_sub, mail_message, to_list):
    try:
        r = requests.post(
            url="https://api.mailgun.net/v3/sandboxb76ec3927a684f8194c2083ff587de40.mailgun.org/messages",
            auth=("api", "key-c035c61e9760229b7c5620068a836532"),
            data={
                "from": u"自强信使 <mailgun@sandboxb76ec3927a684f8194c2083ff587de40.mailgun.org>",
                "to": to_list,
                "subject": mail_sub,
                "text": mail_message
            }
        )
    except RequestException, socket.timeout:
        logger.error(u'Timeout: cannot send email message with subject "%s" and content "%s"' % (mail_sub, mail_message))
        return

    if r.status_code != requests.codes.ok:
        logger.error(u'Error %s: cannot send email message with subject "%s" and content "%s"' % (r.text, mail_sub, mail_message))
    logger.info(u'Successfully sent message: %s' % mail_message)


@app.task(bind=True)
def run(self):
    manager = PluginManager()
    manager.load_plugins()
    for plugin in manager.plugins:
        plugin_instance = plugin['class'](iden=plugin['iden'], dir=plugin['dir'])
        try:
            plugin_instance.process()
        except PluginException:
            logger.exception(u'Error when process plugin %s' % plugin_instance.name)
    logger.info('Successfully ran monitor')
