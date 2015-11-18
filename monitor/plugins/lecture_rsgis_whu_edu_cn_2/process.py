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
        return self.get_soup().find('ul', attrs={'class': 'list lh24 f14'}).find_all('li', attrs={'class': ''})

    def get_title(self, item):
        return unicode(item.select('a')[0].contents[0])

    def get_url(self, item):
        return urljoin(self.url, item.select('a')[0]['href'])

    def get_postdate(self, item):
        return unicode(item.find('span').contents[0])

    def get_content(self, url):
        article = self.get_content_soup(url).find('div', attrs={'id': 'Article'})
        if article:
            return unicode(article.find('div', attrs={'class': 'content'}))
        else:
            return None
