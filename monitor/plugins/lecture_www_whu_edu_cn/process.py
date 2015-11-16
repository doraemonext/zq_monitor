# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

from bs4 import BeautifulSoup

from monitor.plugins.base import PluginProcessor

__all__ = ['Plugin']


class Plugin(PluginProcessor):

    def process(self):
        resp = self.request(self.url)
        print resp.encode('raw_unicode_escape')
        return resp
