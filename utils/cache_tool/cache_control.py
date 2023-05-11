"""
#!/usr/bin/env python
# -*- coding:utf-8 -*-

@Author : Ada
@Time : 2023/4/28 17:25
@Project : ada_pytest_api_project
@File : cache_control.py

"""
# Code starts here...
from utils.exception_tool.exceptions import ValueNotFoundError

_cache_config = {}


class CacheHandler:
    @staticmethod
    def get_cache(cache_data):
        try:
            return _cache_config[cache_data]
        except KeyError:
            raise ValueNotFoundError(f"{cache_data}的缓存数据未找到，请检查是否将该数据存入缓存中")

    @staticmethod
    def update_cache(*, cache_name, value):
        _cache_config[cache_name] = value