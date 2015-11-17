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
        return text

    def get_item_list(self):
        return self.get_soup().find_all('td', attrs={'class': 'list_14'})

    def get_title(self, item):
        first = item.find('a').find('font').find('font')
        if first is None:
            return unicode(item.find('a').find('font').contents[0]).strip()
        else:
            return unicode(first.contents[0]).strip()

    def get_url(self, item):
        return urljoin(self.url, item.select('a')[0]['href'])

    def get_postdate(self, item):
        return unicode(item.find_next('td', attrs={'class': 'time'}).contents[0])

    def get_content(self, url):
        return unicode(self.get_content_soup(url).find('td', attrs={'class': 'con', 'valign': 'top'}))
