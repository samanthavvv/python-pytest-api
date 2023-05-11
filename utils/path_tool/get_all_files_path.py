"""
#!/usr/bin/env python
# -*- coding:utf-8 -*-

@Author : Ada
@Time : 2023/4/28 11:25
@Project : ada_pytest_api_project
@File : get_all_files_path.py

"""
# Code starts here...
import os

from utils.path_tool.set_path import ensure_path_sep


def get_all_files(file_path, excel_data_switch=False, yaml_data_switch=False) -> list:
    """
    获取文件路径
    :param file_path: 目录路径
    :param yaml_data_switch: 是否过滤文件为 yaml格式， True则过滤
    :return: 列表，获取指定的 file_path 路径下的，所有yaml 文件名称
    """
    filename = []
    # 获取所有文件下的子文件名称
    # todo 换成 path 模块去操作
    for root, dirs, files in os.walk(file_path):
        for _file_path in files:
            path = os.path.join(root, _file_path)
            if excel_data_switch:
                if '.xlsx' in path:
                    filename.append(path)
            elif yaml_data_switch:
                if 'yaml' in path or '.yml' in path:
                    filename.append(path)
            else:
                filename.append(path)
    return filename

if __name__ == '__main__':
    file_path = get_all_files(file_path=ensure_path_sep("\data"), excel_data_switch=True)
    print(file_path)