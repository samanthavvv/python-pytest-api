"""
#!/usr/bin/env python
# -*- coding:utf-8 -*-

@Author : Ada
@Time : 2023/5/6 14:49
@Project : ada_pytest_api_project
@File : conftest.py

"""
# Code starts here...
import logging
import time
import pytest

from utils.logging_tool.log_control import INFO


print('*'*30, 'conftest.py')

class RetryCount:
    max_retries = 2  # 最大重跑次数
    retry_count = 0  # 当前重跑次数

def retry_setting(item, result):
    if RetryCount.retry_count < RetryCount.max_retries:
        RetryCount.retry_count += 1
    else:
        setattr(item, 'result', result)
        RetryCount.retry_count = 0


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
        if call.excinfo is not None:
            setattr(item, 'result', 'retry')
            retry_setting(item, 'error')
        elif report.outcome == 'failed' and call.excinfo is None:
            setattr(item, 'result', 'retry')
            retry_setting(item, report.outcome)
        elif report.outcome == 'passed' or report.outcome == 'skipped':
            setattr(item, 'result', report.outcome)
            RetryCount.retry_count = 0

@pytest.fixture(scope="session", autouse=True)
def do_init():
    from utils.initialize_tool.initialize_control import work_login_init,after_login_init_data,load_all_account
    work_login_init(),
    after_login_init_data(),
    load_all_account()

def pytest_collection_modifyitems(items):
    """
    测试用例收集完成时，将收集到的item的name和nodeid的中文显示控制台上
    :return:
    """
    for item in items:
        item.name = item.name.encode("utf-8").decode("unicode_escape")
        item._nodeid = item.nodeid.encode("utf-8").decode("unicode_escape")

def pytest_terminal_summary(terminalreporter):
    """
    收集测试结果
    """

    _PASSED = len([i for i in terminalreporter.stats.get('passed', []) if i.when != 'teardown'])
    _ERROR = len([i for i in terminalreporter.stats.get('error', []) if i.when != 'teardown'])
    _FAILED = len([i for i in terminalreporter.stats.get('failed', []) if i.when != 'teardown'])
    _SKIPPED = len([i for i in terminalreporter.stats.get('skipped', []) if i.when != 'teardown'])
    _TOTAL = terminalreporter._numcollected
    _TIMES = time.time() - terminalreporter._sessionstarttime
    INFO.logger.info(f"用例总数: {_TOTAL}")
    INFO.logger.info(f"通过用例数: {_PASSED}")
    INFO.logger.info(f"异常用例数: {_ERROR}")
    INFO.logger.info(f"失败用例数: {_FAILED}")
    INFO.logger.info(f"跳过用例数: {_SKIPPED}")
    INFO.logger.info("用例执行时长: %.2f" % _TIMES + " s")

    try:
        _RATE = _PASSED / _TOTAL * 100
        INFO.logger.info("用例成功率: %.2f" % _RATE + " %")
    except ZeroDivisionError:
        INFO.logger.info("用例成功率: 0.00 %")


