"""
#!/usr/bin/env python
# -*- coding:utf-8 -*-

@Author : Ada
@Time : 2023/4/28 17:39
@Project : ada_pytest_api_project
@File : yaml_control.py

"""
# Code starts here...
import os
import yaml.scanner



class GetYamlData:
    """ 获取 yaml 文件中的数据 """

    def __init__(self, file_dir):
        self.file_dir = str(file_dir)

    def get_yaml_data(self) -> dict:
        """
        获取 yaml 中的数据
        :param: fileDir:
        :return:
        """
        # 判断文件是否存在
        if os.path.exists(self.file_dir):
            data = open(self.file_dir, 'r', encoding='utf-8')
            res = yaml.load(data, Loader=yaml.FullLoader)
        else:
            raise FileNotFoundError("文件路径不存在")
        return res