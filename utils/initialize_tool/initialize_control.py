"""
#!/usr/bin/env python
# -*- coding:utf-8 -*-

@Author : Ada
@Time : 2023/5/8 18:22
@Project : ada_pytest_api_project
@File : initialize_control.py

"""
# Code starts here...

# 登录
import ast
import logging
import time

import jsonpath
import pytest
import requests

from utils import config
from utils.cache_tool.cache_control import CacheHandler
from utils.logging_tool.log_control import INFO, ERROR
from utils.regular_tool.regular_control import regular, cache_regular



def work_login_init():
    """
    获取登录的cookie
    :return:
    """

    url = f"{config.host}/api/zz/open/UserLogin/login"
    data = {
        "preToken": "",
        "username": f"{config.current_user['user_jm']['username']}",
        "password": f"{config.current_user['user_jm']['password']}",
        "checkCode": "1",
        "rememberMe": "false"

    }

    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json;charset=UTF-8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.44 '
    }

    # 用于 cookie 收集的
    # 请求登录接口
    # cookies = ''
    # for k, v in response_cookie.items():
    #     _cookie = k + "=" + v + ";"
    #     # 拿到登录的cookie内容，cookie拿到的是字典类型，转换成对应的格式
    #     cookies += _cookie
    #     # 将登录接口中的cookie写入缓存中，其中login_cookie是缓存名称

    # 用于 token 收集的
    res = requests.post(url=url, json=data, verify=True, headers=headers)

    # TODO 根据登录是否成功执行后续接口
    if jsonpath.jsonpath(res.json(), '$.code')[0] == '0000':
        authorization = 'Bearer ' + jsonpath.jsonpath(res.json(), '$.data.access_token')[0]
        CacheHandler.update_cache(cache_name='authorization', value=authorization)
        token = {jsonpath.jsonpath(res.json(), '$.data.access_token')[0]}

        success_msg = f"""begin=====================================================
        登录成功，access_token = {token}
        ====================================================== END"""

        INFO.logger.info(success_msg)
    else:
        fail_info = f'\n 未登录成功 {res.json()}'
        ERROR.logger.error(fail_info)
        pytest.exit(f'\n 未登录成功 {fail_info}', returncode=1)


# 登录初始化
def after_login_init_data():
    url = f"{config.host}/api/zz/zz/baseAccountCard/searchInitData?_RET_RAND_TIME_STAMP=${{get_now_time()}}"

    payload = {}
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN',
        'Authorization': '$cache{authorization}',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.54'
    }

    url = regular(url)
    headers = ast.literal_eval(cache_regular(str(headers)))

    res = requests.request("GET", url, headers=headers, data=payload)

    time.sleep(2)

    # TODO 根据初始化是否成功，决定是否执行后续接口
    if jsonpath.jsonpath(res.json(), '$.code')[0] == '0000':
        success_msg = f"""begin=====================================================
        登录初始化成功
        ====================================================== END"""
        INFO.logger.info(success_msg)
    else:
        fail_info = f'\n 登录初始化失败，返回信息 {res.json()}'
        ERROR.logger.error(fail_info)
        pytest.exit(f'\n 登录初始化失败，返回信息 {fail_info}', returncode=1)


# 加载商家账套信息
def load_all_account():
    url = f"{config.host}/api/zz/zz/baseAccountCard/list"

    payload = {}
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN',
        'Authorization': '$cache{authorization}',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.54 '
    }

    url = regular(url)
    headers = ast.literal_eval(cache_regular(str(headers)))

    res = requests.request("GET", url, headers=headers, data=payload)

    time.sleep(2)

    # TODO 根据加载商家账套是否成功，决定是否执行后续接口
    if jsonpath.jsonpath(res.json(), '$.code')[0] == '0000':
        success_msg = f"""begin=====================================================
        加载商家账套信息成功
        ====================================================== END"""
        INFO.logger.info(success_msg)

        # 将所有商家账套信息写入缓存
        acid = jsonpath.jsonpath(res.json(), f'$.data[?(@.accountCode=="{config.account_code}")].id')
        CacheHandler.update_cache(cache_name='acid', value=acid[0])
    else:
        fail_info = f'\n 加载商家账套信息失败，返回信息 {res.json()}'
        ERROR.logger.error(fail_info)
        pytest.exit(f'\n 加载商家账套信息失败，返回信息 {fail_info}', returncode=1)
