"""
#!/usr/bin/env python
# -*- coding:utf-8 -*-

@Author : Ada
@Time : 2023/4/28 11:52
@Project : ada_pytest_api_project
@File : get_excel_data_analysis.py

"""
# Code starts here...
import os
from typing import Union, Text, List

from utils.cache_tool.cache_control import CacheHandler
from utils.excel_tool.excel_control import GetExcelData
from utils.format_data_tool.models import TestCaseEnum, Method, RequestType, TestCase


class CaseDataCheck:
    """
    excel 数据解析, 判断数据填写是否符合规范
    """
    def __init__(self, file_path):
        self.file_path = file_path
        if os.path.exists(self.file_path) is False:
            raise FileNotFoundError("用例地址未找到")

        self.case_data = None
        self.case_id = None

    def _assert(self, attr: Text):
        assert attr in self.case_data.keys(), (
            f"用例ID为 {self.case_id} 的用例中缺少 {attr} 参数，请确认用例内容是否编写规范."
            f"当前用例文件路径：{self.file_path}"
        )

    def check_params_exit(self):
        """
        判断测试用例 excel 文件的每个sheet 中，必须的字段是否都存在
        @return:
        """
        for enum in list(TestCaseEnum._value2member_map_.keys()):   # list(TestCaseEnum._value2member_map_.keys()) ：列表中的每个元素为二元组，例如 'url', True)
            if enum[1]:
                self._assert(enum[0])

    def check_params_right(self, enum_name, attr:str):
        """
        校验一些字段的值，是否在枚举列表中
        :return:
        """
        _member_names_ = enum_name._member_names_
        assert attr.upper() in _member_names_, (
            f"用例ID {self.case_id} 的用例中 {attr} 填写不正确,"
            f"当前框架中，只支持 {_member_names_} 类型."
            f"如需新增 method 类型，请联系管理员"
            f"当前用例文件路径: {self.file_path}"
        )
        return attr.upper()

    @property
    def get_method(self):
        return self.check_params_right(
            Method,
            self.case_data.get(TestCaseEnum.METHOD.value[0])
        )

    @property
    def get_host(self) -> Text:
        host = (
                self.case_data.get(TestCaseEnum.HOST.value[0]) +
                self.case_data.get(TestCaseEnum.URL.value[0])
        )
        return host

    @property
    def get_request_type(self):
        return self.check_params_right(
            RequestType,
            self.case_data.get(TestCaseEnum.REQUEST_TYPE.value[0])
        )

    @property
    def get_dependence_case_data(self):
        """
        暂时用不到。
        :return:
        """
        _dep_data = self.case_data.get(TestCaseEnum.DE_CASE.value[0])
        if _dep_data:
            assert self.case_data.get(TestCaseEnum.DE_CASE_DATA.value[0]) is not None, (
                f"程序中检测到您的 case_id 为 {self.case_id} 的用例存在依赖，但是 {_dep_data} 缺少依赖数据."
                f"如已填写，请检查缩进是否正确， 用例路径: {self.file_path}"
            )
        return self.case_data.get(TestCaseEnum.DE_CASE_DATA.value[0])

    @property
    def get_assert(self):
        _assert_data = self.case_data.get(TestCaseEnum.ASSERT_DATA.value[0])
        assert _assert_data is not None, (
            f"用例ID 为 {self.case_id} 未添加断言，用例路径: {self.file_path}"
        )
        return _assert_data

    @property
    def get_sql(self):
        _sql = self.case_data.get(TestCaseEnum.SQL.value[0])
        # 判断数据库开关为开启状态，并且sql不为空
        # todo 配置文件配置
        # if config.mysql_db.switch and _sql is None:
        #     return None
        return _sql



class CaseData(CaseDataCheck):
    def case_process(self, case_id_switch: Union[None, bool] = None):
        """

        :param case_id_switch:
        :return:
        """
        data = GetExcelData(self.file_path).orgnize_data()
        """data 格式如下,一个字典对应一个sheet
            [
            {'sheet_name':'sheet1', 'feature':'f1', 'case_id1':{},'case_id2':{}},
            {'sheet_name':'sheet2', 'feature':'f1', 'case_id1':{},'case_id2':{}}
            ]
            原来的框架是：一个yaml 文件，返回一个data，格式如下：{'feature':'f1','case_id1':{},'case_id2':{}}
        """
        case_list = []  #

        for sheet in data:
            for key, values in sheet.items():
                if key != 'sheet_name' and key != 'feature':
                    self.case_id = key
                    self.case_data = values
                    super().check_params_exit()
                    case_data ={
                        'parent_case': self.case_data.get(TestCaseEnum.PARENT_CASE.value[0]),
                        'url': self.get_host,
                        'method': self.get_method,
                        'detail': self.case_data.get(TestCaseEnum.DETAIL.value[0]),
                        'is_run': self.case_data.get(TestCaseEnum.IS_RUN.value[0]),
                        'headers': self.case_data.get(TestCaseEnum.HEADERS.value[0]),
                        'requestType': super().get_request_type,
                        'data': self.case_data.get(TestCaseEnum.DATA.value[0]),
                        'dependence_case': self.case_data.get(TestCaseEnum.DE_CASE.value[0]),
                        'dependence_case_data': self.case_data.get(TestCaseEnum.DE_CASE_DATA.value[0]),
                        'assert_data': self.get_assert,
                        'sql': self.get_sql,
                        'setup_sql': self.case_data.get(TestCaseEnum.SETUP_SQL.value[0]),
                        'current_request_set_cache': self.case_data.get(TestCaseEnum.CURRENT_RE_SET_CACHE.value[0]),
                        'teardown': self.case_data.get(TestCaseEnum.TEARDOWN.value[0]),
                        'teardown_sql': self.case_data.get(TestCaseEnum.TEARDOWN_SQL.value[0]),
                        'sleep': self.case_data.get(TestCaseEnum.SLEEP.value[0]),
                    }
                    case_list.append({key: TestCase(**case_data).dict()})

        return case_list



class GetTestCase:

    @staticmethod
    def case_data(case_id_lists: List):
        """

        @param case_id_lists:
        @return:
        """
        case_lists = []
        for i in case_id_lists:
            _data = CacheHandler.get_cache(i)
            case_lists.append(_data)

        return case_lists

if __name__ == '__main__':
     cd = CaseData(r'E:\allProject\ada_pytest_api_project\data\YunKuaiJi\DebugTest\debug_test_query.xlsx')
     print(cd.case_process())
     # for i in cd.case_process():
     #     print(i.keys())
     #     print()
