"""
#!/usr/bin/env python
# -*- coding:utf-8 -*-

@Author : Ada
@Time : 2023/5/9 13:33
@Project : ada_pytest_api_project
@File : log_decorator.py

"""
# Code starts here...

from utils.format_data_tool.models import ResponseData
from .log_control import INFO,ERROR,WARNING

def result_log(test_result, res:ResponseData, log_switch=True):
    if log_switch is True or log_switch is None:
        msg = f"""\n BEGIN ======================================================
        清理api?: {res.is_clear_api} 
        用例标题: {res.detail} 
        请求路径: {res.url} 
        请求方式: {res.method} 
        请求头: {res.headers} 
        请求数据: {res.res_request if test_result!='error' else None} 
        接口响应内容: {res.response_data if test_result!='error' else None} 
        接口响应时长: {res.res_time if test_result!='error' else None} 
        Https状态码: {res.status_code if test_result!='error' else None} 
====================================================== END\n
        """

        if test_result == 'error':
            ERROR.logger.error(msg)
        elif test_result == 'passed':
            INFO.logger.info(msg)
        elif test_result == 'failed':
            WARNING.logger.warning(msg)
        elif test_result == 'skipped':
            INFO.logger.info(msg)