# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

import logging
from urlparse import urljoin

from monitor.plugins.base import PluginProcessor


__all__ = ['Plugin']

logger = logging.getLogger(__name__)


class Plugin(PluginProcessor):

    @staticmethod
    def decode_text(text):
        return text.encode('raw_unicode_escape')

    def get_item_list(self):
        return self.get_soup().find('ul', attrs={'class': 'list'}).find_all('li')

    def get_title(self, item):
        return unicode(item.find('a').contents[0]).strip()

    def get_url(self, item):
        return urljoin(self.url, item.find('a')['href'])

    def get_postdate(self, item):
        return None

    def get_content(self, url):
        soup = self.get_content_soup(url)
        return unicode(soup.find('div', attrs={'class': 'text'}))