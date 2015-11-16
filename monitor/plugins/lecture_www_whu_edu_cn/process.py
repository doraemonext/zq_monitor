# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

from bs4 import BeautifulSoup
from urlparse import urljoin

from monitor.models import Record
from monitor.plugins.base import PluginProcessor
from monitor.tasks import send_message

__all__ = ['Plugin']


class Plugin(PluginProcessor):

    def process(self):
        resp = self.request(self.url).encode('raw_unicode_escape')
        soup = BeautifulSoup(resp)
        title_list = soup.find_all('td', class_='tzggtitle')[1:]
        for title in title_list:
            subject = title.select('a')[0].contents[0]
            url = urljoin(self.url, title.select('a')[0]['href'])
            content_soup = BeautifulSoup(self.request(url).encode('raw_unicode_escape'))
            content = content_soup.find('form', attrs={'name': '_newscontent_fromname'})
            record = Record.objects.add_record(url, content)

        return resp
