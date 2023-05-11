#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time   : 2023-05-05 16:08:55


import pytest

from utils.assert_tool.assert_control import AssertUtil, Assert
from utils.format_data_tool.get_excel_data_analysis import GetTestCase
# from utils.assertion.assert_control import Assert
# from utils.requests_tool.request_control import RequestControl
# from utils.requests_tool.teardown_control import TearDownHandler
from utils.format_data_tool.models import TestCase
from utils.logging_tool.log_control import ERROR
from utils.regular_tool.regular_control import regular
from utils.request_tool.request_control import RequestControl
from utils.logging_tool.log_decorator import result_log

case_id = ['account_init_01', 'clear_query_subject_1999_02', 'clear_delete_subject_1999_03', 'debug_api_04', 'debug_api_create_subject_1999_05', 'debug_api_query_subject_1999_06', 'debug_api_query_subject_1901_07']
TestData = GetTestCase.case_data(case_id)
re_data = regular(str(TestData))

print('开始测试啦')

@pytest.fixture()
def fixture1(request):
    yield request.param
    # request.node: 一个 <class '_pytest.python.Function'> 对象
    result = request.node.result
    res = request.param['res']
    result_log(result, res)

class TestDebugCreateDelete1999:
    
    @pytest.mark.flaky(reruns=2, reruns_delay=2)    
    @pytest.mark.parametrize('fixture1', eval(re_data), ids=[i['detail'] for i in TestData], indirect=True)
    def test_debug_create_delete_1999(self, fixture1):
        """
        :param :
        :return:
        """
        try:
            res = RequestControl(fixture1).http_request()
            fixture1['res'] = res
            Assert(assert_data=fixture1['assert_data'],
                       sql_data=res.sql_data,
                       request_data=res.body,
                       response_data=res.response_data,
                       status_code=res.status_code).assert_type_handle()
        except Exception as e:
            fixture1['res'] = TestCase(**fixture1)
            ERROR.logger.error(e)
            raise e



        # TearDownHandler(res).teardown_handle()
        # Assert(assert_data=in_data['assert_data'],
        #        sql_data=res.sql_data,
        #        request_data=res.body,
        #        response_data=res.response_data,
        #        status_code=res.status_code).assert_type_handle()


if __name__ == '__main__':
    pytest.main(['debug_create_delete_1999', '-s', '-W', 'ignore:Module already imported:pytest.PytestWarning'])
