# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

import logging
from bs4 import BeautifulSoup
from urlparse import urljoin

from monitor.models import Record
from monitor.plugins.base import PluginProcessor
from monitor.plugins.exceptions import PluginRequestError
from monitor.tasks import send_message

__all__ = ['Plugin']

logger = logging.getLogger(__name__)


class Plugin(PluginProcessor):

    def process(self):
        resp = self.request(self.url).encode('raw_unicode_escape').decode('gbk')
        soup = BeautifulSoup(resp)
        item_list = soup.find('div', class_='listmb').find_all('li')
        item_list.reverse()
        for item in item_list:
            title = unicode(item.select('a')[0].contents[0]).strip()
            url = urljoin(self.url, item.select('a')[0]['href'])
            postdate = unicode(item.select('span')[0].contents[0])
            try:
                content_soup = BeautifulSoup(self.request(url).encode('raw_unicode_escape').decode('gbk'))
            except PluginRequestError:
                logger.warning('Cannot access url: %s' % url)
                continue
            content = unicode(content_soup.find('div', attrs={'class': 'showb'}))
            record = Record.objects.add_record(url=url, title=title, content=content, postdate=postdate)
            send_message(record=record, plugin=self.plugin_instance)
