# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

from bs4 import BeautifulSoup

from monitor.plugins.base import PluginProcessor

__all__ = ['Plugin']


class Plugin(PluginProcessor):
    name = '武汉大学主页讲座抓取'
    url = 'http://www.whu.edu.cn/tzgg.htm'

    def process(self):
        return self.request(Plugin.url)
