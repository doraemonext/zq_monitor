# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

import logging
from imp import find_module, load_module, acquire_lock, release_lock
import os
import sys

from django.conf import settings

import requests
from requests.exceptions import RequestException
from bs4 import BeautifulSoup

from monitor.models import Plugin
from monitor.plugins.exceptions import PluginRequestError
from monitor.models import Record

logger = logging.getLogger(__name__)


class PluginProcessor(object):
    """ 爬取插件基类 """

    DEBUG = False  # 是否对本插件开启 DEBUG 模式

    def __init__(self, iden, dir):
        self.plugin_instance = Plugin.objects.get(iden=iden)
        self.iden = iden
        self.dir = dir
        self.url = self.plugin_instance.url

    def process(self):
        item_list = self.get_item_list()
        item_list.reverse()
        if self.DEBUG:
            logger.debug('Plugin iden %s: ' % self.plugin_instance.iden)
        for item in item_list:
            title = self.get_title(item)
            if self.DEBUG:
                logger.debug('\tTitle: %s' % title)
            url = self.get_url(item)
            if self.DEBUG:
                logger.debug('\tURL: %s' % url)
            postdate = self.get_postdate(item)
            if self.DEBUG:
                logger.debug('\tPostdate: %s' % postdate)

            record = Record.objects.filter(url=url)
            if not record.exists():
                try:
                    content = self.get_content(url)
                except PluginRequestError:
                    logger.warning('Cannot access url: %s' % url)
                    continue
                self.insert_record(url=url, title=title, postdate=postdate, content=content)
            else:
                self.insert_record(record=record[0])

            if self.DEBUG:
                logger.debug('-----------------------------')

    @staticmethod
    def decode_text(text):
        return text.encode('raw_unicode_escape')

    def get_fulltext(self):
        return self.decode_text(self.request(self.url))

    def get_soup(self):
        return BeautifulSoup(self.get_fulltext())

    def get_item_list(self):
        return self.get_soup().find_all('td')

    def get_title(self, item):
        raise NotImplementedError('You must implement get_title() method in plugin')

    def get_url(self, item):
        raise NotImplementedError('You must implement get_url() method in plugin')

    def get_postdate(self, item):
        raise NotImplementedError('You must implement get_postdate() method in plugin')

    def get_content_fulltext(self, url):
        return self.decode_text(self.request(url))

    def get_content_soup(self, url):
        return BeautifulSoup(self.get_content_fulltext(url))

    def get_content(self, url):
        raise NotImplementedError('You must implement get_content() method in plugin')

    def insert_record(self, url=None, title=None, content=None, postdate=None, record=None):
        if self.DEBUG:
            return

        from monitor.utils import send_message  # 解决循环导入问题
        if record:
            send_message(record=record, plugin=self.plugin_instance)
            return

        if not content:
            content = '外部链接, 请打开上述网址'
        if not postdate:
            postdate = ''
        record = Record.objects.add_record(url=url, title=title, content=content, postdate=postdate)
        send_message(record=record, plugin=self.plugin_instance)

    @staticmethod
    def request(url, timeout=settings.MONITOR_DEFAULT_TIMEOUT):
        try:
            r = requests.get(url, timeout=timeout)
        except RequestException as e:
            raise PluginRequestError(e)
        return r.text


class PluginManager(object):
    """ 目录加载型 插件管理器 """

    def __init__(self):
        self.__directory = os.path.join(settings.BASE_DIR, "monitor/plugins")
        self.__plugins = []
        super(PluginManager, self).__init__()

    @property
    def plugins(self):
        return self.__plugins

    def load_plugins(self):
        """ 搜索并加载插件目录中的所有插件 """

        logger.debug('Start loading plugin from directory')

        plugins = []
        plugins_list = Plugin.objects.filter(status=True).values()
        for plugin in plugins_list:
            filename = plugin['iden']
            try:
                full_path = os.path.join(self.__directory, filename)
                if os.path.isdir(full_path) and os.path.exists(os.path.join(full_path, "process.py")):
                    plugins.append((filename, self.__directory))
            except OSError:
                logger.exception('Load plugins error: Failed to access plugin file')

        fh = None
        mod = None
        for (iden, dir) in plugins:
            try:
                acquire_lock()
                fh, filename, desc = find_module("process", [os.path.join(dir, iden)])
                old = sys.modules.get(iden)
                if old is not None:
                    del sys.modules[iden]
                mod = load_module(iden, fh, filename, desc)
            finally:
                if fh:
                    fh.close()
                release_lock()
            if hasattr(mod, "__all__"):
                attrs = [getattr(mod, x) for x in mod.__all__]
                for plug in attrs:
                    if issubclass(plug, PluginProcessor):
                        self.__plugins.append({
                            'iden': iden,
                            'dir': dir,
                            'class': plug,
                        })

        logger.debug('Finished loading plugin from directory')
