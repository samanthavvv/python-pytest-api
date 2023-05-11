#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time   : 2023-05-05 16:08:55


import allure
import pytest
from utils.read_files_tools.get_yaml_data_analysis import GetTestCase
from utils.assertion.assert_control import Assert
from utils.requests_tool.request_control import RequestControl
from utils.read_files_tools.regular_control import regular
from utils.requests_tool.teardown_control import TearDownHandler


case_id = ['account_init_011', 'clear_query_subject_1999_022', 'clear_delete_subject_1999_033', 'debug_api_044', 'debug_api_create_subject_1999_055', 'debug_api_query_subject_1999_066', 'debug_api_query_subject_1901_077', 'debug_api_delete_subject_1999_088']
TestData = GetTestCase.case_data(case_id)
re_data = regular(str(TestData))


class TestDebugCreateDelete199901:
    
    @pytest.mark.flaky(reruns=2, reruns_delay=2)    
    @pytest.mark.parametrize('in_data', eval(re_data), ids=[i['detail'] for i in TestData])
    def test_debug_create_delete_1999_01(self, in_data, case_skip):
        """
        :param :
        :return:
        """
        res = RequestControl(in_data).http_request()
        TearDownHandler(res).teardown_handle()
        Assert(assert_data=in_data['assert_data'],
               sql_data=res.sql_data,
               request_data=res.body,
               response_data=res.response_data,
               status_code=res.status_code).assert_type_handle()


if __name__ == '__main__':
    pytest.main(['debug_create_delete_1999_01', '-s', '-W', 'ignore:Module already imported:pytest.PytestWarning'])
