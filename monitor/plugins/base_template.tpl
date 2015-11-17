# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

import logging
from urlparse import urljoin

from monitor.plugins.base import PluginProcessor


__all__ = ['Plugin']

logger = logging.getLogger(__name__)


class Plugin(PluginProcessor):

    # 该方法仅在默认方式获取目标网页乱码时才需手动设置, 默认可以删掉不写
    @staticmethod
    def decode_text(text):
        return text.encode('raw_unicode_escape')

    def get_item_list(self):
        pass  # 获取项目列表并返回

    def get_title(self, item):
        pass  # 根据单个项目获取标题

    def get_url(self, item):
        pass  # 根据单个项目获取目标 URL

    def get_postdate(self, item):
        pass  # 根据单个项目获取发布日期

    def get_content(self, url):
        pass  # 根据目标 URL 获取目标内容
