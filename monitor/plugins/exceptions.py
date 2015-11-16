# -*- coding: utf-8 -*-


class PluginException(Exception):
    pass


class PluginRequestError(PluginException):
    """ 插件请求网络错误 """
    pass
