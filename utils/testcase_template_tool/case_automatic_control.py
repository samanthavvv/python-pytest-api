"""
#!/usr/bin/env python
# -*- coding:utf-8 -*-

@Author : Ada
@Time : 2023/5/4 14:51
@Project : ada_pytest_api_project
@File : case_automatic_control.py

"""
# Code starts here...
from typing import Text

from utils import ensure_path_sep
from utils.excel_tool.excel_control import GetExcelData
from utils.exception_tool.exceptions import TestCaseFileTypeError
from utils.path_tool.get_all_files_path import get_all_files
from pathlib import Path

from utils.testcase_template_tool.testcase_template import write_testcase_file


class TestCaseAutomaticGeneration:

    def mk_dir(self, file_path):
        """
        当测试用例 .py 文件的父目录不存在时，则创建
        :param file_path:
        :return:
        """
        data_path = file_path.replace(ensure_path_sep(r'/data'), '')  # 例如 \YunKuaiJi\DebugTest\debug_test_query.xlsx
        p_dir = Path(ensure_path_sep('/test_case'))  # 例如 E:\allProject\ada_pytest_api_project\test_case
        # todo 应该使用 pathlib 模块的路径拼接方法，而不是直接字符串拼接
        _case_dir_path = Path(
            str(p_dir) + str(data_path)).parent  # 例如 E:\allProject\ada_pytest_api_project\test_case\YunKuaiJi\DebugTest

        if not _case_dir_path.exists():
            _case_dir_path.mkdir(parents=True, exist_ok=True)  # 如果目录不存在，则创建

    def get_case_dir_and_filename(self,file_path, sheet_name):
        data_path = file_path.replace(ensure_path_sep(r'/data'), '')  # 例如 \YunKuaiJi\DebugTest\debug_test_query.xlsx
        case_root_dir = Path(ensure_path_sep('/test_case'))  # 例如 E:\allProject\ada_pytest_api_project\test_case
        case_path = Path(str(case_root_dir) + str(data_path))

        if case_path.suffix == '.xlsx':
            case_path = case_path.with_name('test_' + f'{sheet_name}' + '.py')
        else:
            raise '测试用例文件必须为 .xlsx 文件'
        return case_path

    def class_title(self, sheet_name: Text) -> Text:
        """
        生成测试用例.py 文件中的类名称
        :param sheet_name:
        :return:
        """
        file_name = sheet_name
        name_words = file_name.split('_')
        _name_len = len(name_words)

        for i in range(_name_len):
            name_words[i] = name_words[i].capitalize()

        _class_name = "".join(name_words)

        return _class_name

    def func_title(self, sheet_name: Text) -> Text:
        """
        测试用例 .py 文件中的函数名称
        :param sheet_name: excel文件中的sheet 名称
        :return:
        """
        file_name = sheet_name  # test_debug_test_query.py
        func_name = file_name.replace('.py', '')

        return func_name

    def case_ids(self, test_case: dict):
        """
        获取每个excel 文件中，每个sheet 中的所有case_id
        :return:
        """
        ids = []
        for k, v in test_case.items():
            if k != 'feature' and k != 'sheet_name':
                ids.append(k)
        return ids

    def get_case_automatic(self):
        file_path = get_all_files(file_path=ensure_path_sep("\\data"), excel_data_switch=True)  # 列表。每个excel 文件的绝对路径
        for file in file_path:
            # 判断用例需要的文件夹路径是否存在？不存在，则创建
            self.mk_dir(file)
            all_test_case = GetExcelData(
                file).orgnize_data()  # [{'sheet_name':xx, 'feature':xx, 'case_id1':xx, 'case_id2':xx,...}]
            for sheet in all_test_case:
                write_testcase_file(
                    class_title=self.class_title(sheet['sheet_name']),
                    func_title=self.func_title(sheet['sheet_name']),
                    case_path=self.get_case_dir_and_filename(file, sheet['sheet_name']),
                    case_ids=self.case_ids(sheet),
                    file_name=sheet['sheet_name']
                )


if __name__ == '__main__':
    # TestCaseAutomaticGeneration().get_case_dir_and_filename(r'E:\allProject\ada_pytest_api_project\data\YunKuaiJi\DebugTest2\debug_test_query2.xlsx','sheet123')
    TestCaseAutomaticGeneration().get_case_automatic()