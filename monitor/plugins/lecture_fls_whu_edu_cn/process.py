# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

import logging
from urlparse import urljoin

from monitor.plugins.base import PluginProcessor
from monitor.plugins.exceptions import PluginRequestError


__all__ = ['Plugin']

logger = logging.getLogger(__name__)


class Plugin(PluginProcessor):

    @staticmethod
    def decode_text(text):
        return text

    def get_item_list(self):
        item_list = self.get_soup().find('div', attrs={'class': 'nei-right'})
        if item_list:
            return item_list.find_all('li')
        else:
            raise PluginRequestError()

    def get_title(self, item):
        return unicode(item.select('a')[0].contents[0]).strip()

    def get_url(self, item):
        return urljoin(self.url, item.select('a')[0]['href'])

    def get_postdate(self, item):
        return unicode(item.find('span').contents[0])

    def get_content(self, url):
        return unicode(self.get_content_soup(url).find('div', attrs={'class': 'text-detail'}))
