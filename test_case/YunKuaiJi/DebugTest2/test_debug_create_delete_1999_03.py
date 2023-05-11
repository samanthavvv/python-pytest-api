#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time   : 2023-05-11 16:24:00


import pytest
from utils.assert_tool.assert_control import Assert
from utils.format_data_tool.get_excel_data_analysis import GetTestCase
from utils.regular_tool.regular_control import regular
from utils.request_tool.request_control import RequestControl


case_id = ['account_init_01111', 'clear_query_subject_1999_02222', 'clear_delete_subject_1999_03333', 'debug_api_04444', 'debug_api_create_subject_1999_05555', 'debug_api_query_subject_1999_06666', 'debug_api_query_subject_1901_07777', 'debug_api_delete_subject_1999_08888']
TestData = GetTestCase.case_data(case_id)
re_data = regular(str(TestData))


class TestDebugCreateDelete199903:

    @pytest.mark.flaky(reruns=2, reruns_delay=2)    
    @pytest.mark.dependency()
    def test_account_init_01111(self, in_data, case_skip):
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
               status_code=res.status_code).assert_type_handle()

    @pytest.mark.flaky(reruns=2, reruns_delay=2)    
    @pytest.mark.dependency()
    def test_clear_query_subject_1999_02222(self, in_data, case_skip):
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
               status_code=res.status_code).assert_type_handle()

    @pytest.mark.flaky(reruns=2, reruns_delay=2)    
    @pytest.mark.dependency(depends=["test_clear_query_subject_1999_02222"])
    def test_clear_delete_subject_1999_03333(self, in_data, case_skip):
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
               status_code=res.status_code).assert_type_handle()

    @pytest.mark.flaky(reruns=2, reruns_delay=2)    
    @pytest.mark.dependency()
    def test_debug_api_04444(self, in_data, case_skip):
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
               status_code=res.status_code).assert_type_handle()

    @pytest.mark.flaky(reruns=2, reruns_delay=2)    
    @pytest.mark.dependency()
    def test_debug_api_create_subject_1999_05555(self, in_data, case_skip):
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
               status_code=res.status_code).assert_type_handle()

    @pytest.mark.flaky(reruns=2, reruns_delay=2)    
    @pytest.mark.dependency()
    def test_debug_api_query_subject_1999_06666(self, in_data, case_skip):
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
               status_code=res.status_code).assert_type_handle()

    @pytest.mark.flaky(reruns=2, reruns_delay=2)    
    @pytest.mark.dependency()
    def test_debug_api_query_subject_1901_07777(self, in_data, case_skip):
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
               status_code=res.status_code).assert_type_handle()

    @pytest.mark.flaky(reruns=2, reruns_delay=2)    
    @pytest.mark.dependency()
    def test_debug_api_delete_subject_1999_08888(self, in_data, case_skip):
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
               status_code=res.status_code).assert_type_handle()
