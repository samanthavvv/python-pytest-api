"""
#!/usr/bin/env python
# -*- coding:utf-8 -*-

@Author : Ada
@Time : 2023/5/11 15:30
@Project : ada_pytest_api_project
@File : testcase_template_v2.py

"""


# Code starts here...
import datetime
import os

from utils import GetYamlData, ensure_path_sep
from utils.exception_tool.exceptions import ValueNotFoundError

conf_data = GetYamlData(ensure_path_sep("\\common\\config.yaml")).get_yaml_data()
now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
real_time_update_test_cases = conf_data['real_time_update_test_cases']

class Template:
    def __init__(self, sheet_cases, class_title, case_path, case_ids, file_name):
        """

        :param sheet_cases: 每个sheet 中的所有接口信息
        :param class_title: 类名
        :param case_path: 测试py 文件路径
        :param case_ids: 每个sheet 中的所有case_id字段的值
        :param file_name: 文件名称
        """
        print(12345,sheet_cases)
        self.sheet_cases = sheet_cases  # {'sheet_name':xx, 'feature':xx, 'case_id1':xx, 'case_id2':xx,...}
        self.class_title = class_title
        self.case_path = case_path
        self.case_ids = case_ids
        self.file_name = file_name

    @property
    def get_case_parent(self):
        case_list = []
        # {'sheet_name': xx, 'feature': xx, 'case_id1': xx, 'case_id2': xx, ...}
        for name,value in self.sheet_cases.items():
            if name != 'feature' and name != 'sheet_name':
                case_list.append((name, value['parent_case']))
        return case_list

    def test_method(self, case_id, parent):
        parent = f'@pytest.mark.dependency(depends=["test_{parent}"])' if parent is not None else f'@pytest.mark.dependency()'

        test_method = f'''
    @pytest.mark.flaky(reruns=2, reruns_delay=2)    
    {parent}
    def test_{case_id}(self, in_data, case_skip):
        """
        :param :
        :return:
        """
        res = RequestControl(in_data).http_request()
        # TearDownHandler(res).teardown_handle()
        Assert(assert_data=in_data['assert_data'],
               sql_data=res.sql_data,
               request_data=res.body,
               response_data=res.response_data,
               status_code=res.status_code).assert_type_handle()\n'''
        return test_method

    @property
    def page(self):
        _page = f'''#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time   : {now}


import pytest
from utils.assert_tool.assert_control import Assert
from utils.format_data_tool.get_excel_data_analysis import GetTestCase
from utils.regular_tool.regular_control import regular
from utils.request_tool.request_control import RequestControl


case_id = {self.case_ids}
TestData = GetTestCase.case_data(case_id)
re_data = regular(str(TestData))


class Test{self.class_title}:\n'''

        for i in self.get_case_parent:
            _page += self.test_method(i[0],i[1])
        return _page

    def write_case(self, case_path, page):
        """ 写入用例数据 """
        with open(case_path, 'w+', encoding="utf-8") as file:
            file.write(page)

    def write_testcase_file(self):
        _page = self.page
        if real_time_update_test_cases:
            self.write_case(case_path=self.case_path, page=_page)
        elif real_time_update_test_cases is False:
            if not os.path.exists(self.case_path):
                self.write_case(case_path=self.case_path, page=_page)
        else:
            raise ValueNotFoundError("real_time_update_test_cases 配置不正确，只能配置 True 或者 False")
