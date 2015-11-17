# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

import logging
from bs4 import BeautifulSoup
from urlparse import urljoin

from monitor.models import Record
from monitor.plugins.base import PluginProcessor
from monitor.plugins.exceptions import PluginRequestError
from monitor.utils import send_message

__all__ = ['Plugin']

logger = logging.getLogger(__name__)


class Plugin(PluginProcessor):

    @staticmethod
    def decode_text(text):
        return text.encode('raw_unicode_escape').decode('gbk')

    def get_item_list(self):
        return self.get_soup().find('div', class_='listmb').find_all('li')

    def get_title(self, item):
        return unicode(item.select('a')[0].contents[0]).strip()

    def get_url(self, item):
        return urljoin(self.url, item.select('a')[0]['href'])

    def get_postdate(self, item):
        return unicode(item.select('span')[0].contents[0])

    def get_content(self, url):
        return unicode(self.get_content_soup(url).find('div', attrs={'class': 'showb'}))
