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
        return text.encode('raw_unicode_escape').decode('gbk')

    def get_item_list(self):
        return self.get_soup().find_all('td', attrs={'align': 'left', 'width': '620'})

    def get_title(self, item):
        return unicode(item.select('a')[0].contents[0])

    def get_url(self, item):
        return urljoin(self.url, item.select('a')[0]['href'])

    def get_postdate(self, item):
        return unicode(item.find_next('td').contents[0])

    def get_content(self, url):
        try:
            return unicode(self.get_content_soup(url).find_all('div', attrs={'id': 'newscontent'})[1])
        except Exception as e:
            logger.exception('Error when get content from lecture_bio_whu_edu_cn plugin, url: %s' % url)
            return None
