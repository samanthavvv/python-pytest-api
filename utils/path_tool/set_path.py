"""
#!/usr/bin/env python
# -*- coding:utf-8 -*-

@Author : Ada
@Time : 2023/4/28 11:07
@Project : ada_pytest_api_project
@File : set_path.py

"""
# Code starts here...
import os
from typing import Text


def root_path():
    """
    获取根路径
    :return: str。项目根路径
    """
    path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    return path     # E:\allProject\ada_pytest_api_project

def ensure_path_sep(path: Text) -> Text:
    path = os.sep.join(path.split("/"))
    return root_path() + path

if __name__ == '__main__':
    print(ensure_path_sep('/debug_test'))