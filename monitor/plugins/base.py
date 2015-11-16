# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

import logging
import traceback
import time
from imp import find_module, load_module, acquire_lock, release_lock
import os
import sys

from django.conf import settings

import requests
from requests.exceptions import RequestException

from monitor.models import Plugin
from monitor.plugins.exceptions import PluginRequestError

logger = logging.getLogger(__name__)


class PluginProcessor(object):
    """ 爬取插件基类 """

    def __init__(self, iden, dir):
        self.plugin_instance = Plugin.objects.get(iden=iden)
        self.iden = iden
        self.dir = dir
        self.url = self.plugin_instance.url

    def process(self):
        raise NotImplementedError('You must implement process() method in plugin')

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
