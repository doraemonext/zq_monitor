# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

import logging
from urlparse import urljoin

from monitor.plugins.base import PluginProcessor


__all__ = ['Plugin']

logger = logging.getLogger(__name__)


class Plugin(PluginProcessor):

    def get_item_list(self):
        return self.get_soup().find('ul', class_='list').find_all('li')

    def get_title(self, item):
        return item.select('a')[0]['title']

    def get_url(self, item):
        return urljoin(self.url, item.select('a')[0]['href'])

    def get_postdate(self, item):
        return item.find('span').contents[0]

    def get_content(self, url):
        return unicode(self.get_content_soup(url).find('div', attrs={'id': 'vsb_content'}))
