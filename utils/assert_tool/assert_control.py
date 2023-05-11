"""
#!/usr/bin/env python
# -*- coding:utf-8 -*-

@Author : Ada
@Time : 2023/5/10 16:00
@Project : ada_pytest_api_project
@File : assert_control.py

"""
# Code starts here...
import ast
import json
from typing import Any, Text

from jsonpath import jsonpath

from utils import config
from utils.assert_tool import assert_type
from utils.exception_tool.exceptions import AssertTypeError
from utils.format_data_tool.models import  AssertMethod, load_module_functions, ResponseData
from utils.logging_tool.log_control import ERROR, WARNING
from utils.regular_tool.regular_control import cache_regular


class AssertUtil:

    def __init__(self, assert_data, sql_data, request_data, response_data, status_code):

        self.response_data = response_data
        self.request_data = request_data
        self.sql_data = sql_data
        self.assert_data = assert_data
        self.sql_switch = config.mysql_db.switch
        self.status_code = status_code

    @staticmethod
    def literal_eval(attr):
        return ast.literal_eval(cache_regular(str(attr)))

    @property
    def get_assert_data(self):
        assert self.assert_data is not None, (
                "'%s' should either include a `assert_data` attribute, "
                % self.__class__.__name__
        )
        return ast.literal_eval(cache_regular(str(self.assert_data)))

    @property
    def get_type(self):
        assert 'type' in self.get_assert_data.keys(), (
            " 断言数据: '%s' 中缺少 `type` 属性 " % self.get_assert_data
        )

        # 获取断言类型对应的枚举值
        name = AssertMethod(self.get_assert_data.get("type")).name
        return name

    @property
    def get_value(self):
        assert 'value' in self.get_assert_data.keys(), (
            " 断言数据: '%s' 中缺少 `value` 属性 " % self.get_assert_data
        )
        return self.get_assert_data.get("value")

    @property
    def get_jsonpath(self):
        assert 'jsonpath' in self.get_assert_data.keys(), (
            " 断言数据: '%s' 中缺少 `jsonpath` 属性 " % self.get_assert_data
        )
        return self.get_assert_data.get("jsonpath")

    @property
    def get_assert_type(self):
        assert 'AssertType' in self.get_assert_data.keys(), (
            " 断言数据: '%s' 中缺少 `AssertType` 属性 " % self.get_assert_data
        )
        return self.get_assert_data.get("AssertType")

    @property
    def get_message(self):
        """
        获取断言描述，如果未填写，则返回 `None`
        :return:
        """
        return self.get_assert_data.get("message", None)

    @property
    def get_sql_data(self):

        # 判断数据库开关为开启，并需要数据库断言的情况下，未编写sql，则抛异常
        if self.sql_switch_handle:
            assert self.sql_data != {'sql': None}, (
                "请在用例中添加您要查询的SQL语句。"
            )

        # 处理 mysql查询出来的数据类型如果是bytes类型，转换成str类型
        if isinstance(self.sql_data, bytes):
            return self.sql_data.decode('utf=8')

        sql_data = jsonpath(self.sql_data, self.get_value)
        assert sql_data is not False, (
            f"数据库断言数据提取失败，提取对象: {self.sql_data} , 当前语法: {self.get_value}"
        )
        if len(sql_data) > 1:
            return sql_data
        return sql_data[0]

    @staticmethod
    def functions_mapping():
        return load_module_functions(assert_type)

    @property
    def get_response_data(self):
        return json.loads(self.response_data)

    @property
    def sql_switch_handle(self):
        """
        判断数据库开关，如果未开启，则打印断言部分的数据
        :return:
        """
        if self.sql_switch is False:
            WARNING.logger.warning(
                "检测到数据库状态为关闭状态，程序已为您跳过此断言，断言值:%s" % self.get_assert_data
            )
        return self.sql_switch

    def _assert(self, check_value: Any, expect_value: Any, message: Text = ""):

        self.functions_mapping()[self.get_type](check_value, expect_value, str(message))

    @property
    def _assert_resp_data(self):
        resp_data = jsonpath(self.get_response_data, self.get_jsonpath)
        assert resp_data is not False, (
            f"jsonpath数据提取失败，提取对象: {self.get_response_data} , 当前语法: {self.get_jsonpath}"
        )
        if len(resp_data) > 1:
            return resp_data
        return resp_data[0]

    @property
    def _assert_request_data(self):
        req_data = jsonpath(self.request_data, self.get_jsonpath)
        assert req_data is not False, (
            f"jsonpath数据提取失败，提取对象: {self.request_data} , 当前语法: {self.get_jsonpath}"
        )
        if len(req_data) > 1:
            return req_data
        return req_data[0]

    def assert_type_handle(self):

        # 判断请求参数数据库断言
        if self.get_assert_type == "R_SQL":
            self._assert(self._assert_request_data, self.get_sql_data, self.get_message)

        # 判断请求参数为响应数据库断言
        elif self.get_assert_type == "SQL" or self.get_assert_type == "D_SQL":
            self._assert(self._assert_resp_data, self.get_sql_data, self.get_message)

        # 判断非数据库断言类型
        elif self.get_assert_type is None or self.get_assert_type == '':
            self._assert(self._assert_resp_data, self.get_value, self.get_message)
        else:
            raise AssertTypeError("断言失败，目前只支持数据库断言和响应断言")


class Assert(AssertUtil):
    """
        assert:
          status_code: 200
          errorCode:
            jsonpath: $.errorCode
            type: ==
            value: -1001
            AssertType:
          errorMsg:
            jsonpath: $.errorMsg
            type: ==
            value: '请先登录！'
            AssertType:
          do_time:
            jsonpath: $.times   # jsonpath 拿到接口响应的数据
            type: ==
            value: $.do_time    # sql 查出来的数据，是字典类型的，因此这里是从字段中提取查看出来的字段
            AssertType: SQL     # 断言sql的时候，AssertType 的值需要填写成 SQL
        sql:
          - select * from users;
          - select * from goods;

    """
    def assert_data_list(self):
        assert_list = []
        for k, v in self.assert_data.items():
            if k == "status_code":
                assert self.status_code == v, "响应状态码断言失败"
            else:
                assert_list.append(v)
        return assert_list

    def assert_type_handle(self):
        for i in self.assert_data_list():   # 例如：i={jsonpath: $.data[1].subjectCode,type: ==,value: 7000_g0,AssertType:None}
            self.assert_data = i
            super().assert_type_handle()



