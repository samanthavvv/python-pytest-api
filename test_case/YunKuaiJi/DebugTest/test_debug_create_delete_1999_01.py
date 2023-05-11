#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time   : 2023-05-11 16:24:00


import pytest
from utils.assert_tool.assert_control import Assert
from utils.format_data_tool.get_excel_data_analysis import GetTestCase
from utils.regular_tool.regular_control import regular
from utils.request_tool.request_control import RequestControl


case_id = ['account_init_011', 'clear_query_subject_1999_022', 'clear_delete_subject_1999_033', 'debug_api_044', 'debug_api_create_subject_1999_055', 'debug_api_query_subject_1999_066', 'debug_api_query_subject_1901_077', 'debug_api_delete_subject_1999_088']
TestData = GetTestCase.case_data(case_id)
re_data = regular(str(TestData))


class TestDebugCreateDelete199901:

    @pytest.mark.flaky(reruns=2, reruns_delay=2)    
    @pytest.mark.dependency()
    def test_account_init_011(self, in_data, case_skip):
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
    def test_clear_query_subject_1999_022(self, in_data, case_skip):
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
    @pytest.mark.dependency(depends=["test_clear_query_subject_1999_022"])
    def test_clear_delete_subject_1999_033(self, in_data, case_skip):
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
    def test_debug_api_044(self, in_data, case_skip):
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
    def test_debug_api_create_subject_1999_055(self, in_data, case_skip):
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
    def test_debug_api_query_subject_1999_066(self, in_data, case_skip):
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
    def test_debug_api_query_subject_1901_077(self, in_data, case_skip):
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
    def test_debug_api_delete_subject_1999_088(self, in_data, case_skip):
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
