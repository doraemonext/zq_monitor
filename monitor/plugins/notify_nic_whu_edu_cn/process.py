# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

import logging
from urlparse import urljoin

from monitor.plugins.base import PluginProcessor


__all__ = ['Plugin']

logger = logging.getLogger(__name__)


class Plugin(PluginProcessor):

    @staticmethod
    def decode_title_text(text):
        return text

    @staticmethod
    def decode_content_text(text):
        return text.encode('raw_unicode_escape')

    def get_item_list(self):
        return self.get_soup(decode_func=Plugin.decode_title_text).find_all('a', attrs={'class': 'c9967'})

    def get_title(self, item):
        return unicode(item.contents[0]).strip()

    def get_url(self, item):
        return urljoin(self.url, item['href'])

    def get_postdate(self, item):
        return None

    def get_content(self, url):
        soup = self.get_content_soup(url, decode_func=Plugin.decode_content_text)
        return unicode(soup.find('div', attrs={'id': 'vsb_newscontent'}))
