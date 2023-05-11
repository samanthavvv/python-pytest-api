"""
#!/usr/bin/env python
# -*- coding:utf-8 -*-

@Author : Ada
@Time : 2023/5/5 16:33
@Project : ada_pytest_api_project
@File : run.py.py

"""
# Code starts here...
import pytest


def run():
    import test_case
    pytest.main(['-vvv', '-s',
                 r'E:\allProject\ada_pytest_api_project\test_case\YunKuaiJi\DebugTest\test_debug_create_delete_1999.py'])

if __name__ == '__main__':
    run()