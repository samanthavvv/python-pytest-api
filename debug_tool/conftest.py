"""
#!/usr/bin/env python
# -*- coding:utf-8 -*-

@Author : Ada
@Time : 2023/5/9 14:35
@Project : ada_pytest_api_project
@File : conftest.py.py

"""
# Code starts here...

import pytest


class RetryCount:
    max_retries = 2  # 最大重跑次数
    retry_count = 0  # 当前重跑次数


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    """
    :param item: 一个 <class '_pytest.python.Function'> 对象
    :param call:
    :return:
    """
    # 每次执行一个测试用例，都会获取钩子方法的调用结果: setup的结果，call的结果，teardown的结果
    out = yield
    if call.when == 'call':
        report = out.get_result()
        if report.outcome == 'failed':
            print('~' * 30, 'pytest_runtest_makereport 开始重试')
            if RetryCount.retry_count < RetryCount.max_retries:
                RetryCount.retry_count += 1
            else:
                setattr(item, 'result', report.outcome)
                RetryCount.retry_count = 0
        elif report.outcome == 'passed':
            setattr(item, 'result', report.outcome)
            RetryCount.retry_count = 0
        elif report.outcome == 'skipped':
            setattr(item, 'result', report.outcome)
            RetryCount.retry_count = 0
