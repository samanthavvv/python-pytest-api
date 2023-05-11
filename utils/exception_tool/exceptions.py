"""
#!/usr/bin/env python
# -*- coding:utf-8 -*-

@Author : Ada
@Time : 2023/4/28 17:26
@Project : ada_pytest_api_project
@File : exceptions.py

"""


# Code starts here...

class MyBaseFailure(Exception):
    pass

class ValueNotFoundError(MyBaseFailure):
    """ 测试用例缓存中，没有对应的缓存 """
    pass

class TestCaseFileTypeError(MyBaseFailure):
    """ 测试用例文件类型错误 """
    pass

class DataAcquisitionFailed(MyBaseFailure):
    pass


class ValueTypeError(MyBaseFailure):
    pass

class AssertTypeError(MyBaseFailure):
    pass
