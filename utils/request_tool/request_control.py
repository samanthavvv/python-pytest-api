"""
#!/usr/bin/env python
# -*- coding:utf-8 -*-

@Author : Ada
@Time : 2023/5/5 16:43
@Project : ada_pytest_api_project
@File : request_control.py

"""
# Code starts here...
import ast
import json
import logging
import os.path
import random
import time
from typing import Dict, Text, Union

import requests
from utils import ensure_path_sep, config
from utils.cache_tool.cache_control import CacheHandler
from utils.format_data_tool.models import TestCase, RequestType, ResponseData
from utils.logging_tool.log_control import ERROR
from utils.mysql_tool.mysql_control import AssertSqlExecution
from utils.regular_tool.regular_control import cache_regular
from requests_toolbelt import MultipartEncoder
from requests import Response

logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)

class RequestControl:
    """ 封装请求 """

    def __init__(self, yaml_case):
        self.__yaml_case = TestCase(**yaml_case)

    def check_headers_str_null(self, headers):
        """
        兼容用户未填写headers或者header值为int
        @return:
        """
        # todo
        # CacheHandler.update_cache(cache_name='authorization', value='12345')
        # CacheHandler.update_cache(cache_name='acid', value='123456')
        # CacheHandler.update_cache(cache_name='1999_id', value='1234567')

        headers = ast.literal_eval(cache_regular(str(headers)))
        if headers is None:
            headers = {"headers": None}
        else:
            for key, value in headers.items():
                if not isinstance(value, str):
                    headers[key] = str(value)
        return headers

    def multipart_in_headers(
            self,
            request_data: Dict,
            header: Dict):
        """
        判断处理header为 Content-Type: multipart/form-data
        :param request_data: 请求body
        :param header: 请求头
        :return:
        """

        if "multipart/form-data" in str(header.values()):
            if request_data and isinstance(request_data, dict):
                for k, v in request_data.items():
                    if not isinstance(v, str):
                        request_data[k] = str(v)
                request_data = MultipartEncoder(request_data)
                header['Content-Type'] = request_data.content_type

        return request_data, header

    def file_api_with_data(self, file_data):
        """
        处理文件上传接口，除了文件上传外，还有其它请求数据时
        :param file_data:
        :return:
        """
        try:
            _data = self.__yaml_case.data
            if _data['data']:
                for key, value in ast.literal_eval(cache_regular(str(_data)))['data'].items():  # 只取data 对应的值
                    if "multipart/form-data" in str(self.__yaml_case.headers.values()):
                        file_data[key] = str(value)
                    else:
                        file_data[key] = value
        except KeyError:
            ...

    def multipart_data(
            self,
            file_data: Dict):
        """ 处理上传文件数据 """
        multipart = MultipartEncoder(
            fields=file_data,  # 字典格式
            boundary='----' + str(random.randint(int(1e28), int(1e29 - 1)))
        )
        return multipart

    def file_prams_exit(self):
        """
        处理文件上传接口，请求数据中是否有 params 参数，需要进行路径拼接
        :return:
        """
        try:
            params = self.__yaml_case.data['params']
        except KeyError:
            params = None
        return params

    def upload_file(self):
        """
        处理接口为上传文件接口。组织请求数据格式，使其符合Content-type="multipart/form-data" 类型
        :return:
        """

        """
                data:
                    requestType: file
                    # 是否执行，空或者 true 都会执行
                    is_run:
                    data:
                      file:
                         排入水体名: 排入水体名.png
                      data:
                         is_upload: 0
                         id: WU_FILE_0
                         lastModifiedDate: 2019/10/16
                         type: application/octet-stream
                      params:
                         collect: false
                         id: WU_FILE_0
        """

        file_data = {}
        self.file_api_with_data(file_data)  # 处理文件数据外的其它请求数据
        _data = self.__yaml_case.data

        for key, value in ast.literal_eval(cache_regular(str(_data)))['file'].items():
            file_path = ensure_path_sep("\\Files\\" + value)
            file_data[key] = (value, open(file_path, 'rb'), 'application/octet-stream')

        multipart = self.multipart_data(file_data)
        self.__yaml_case.headers['Content-Type'] = multipart.content_type
        params_data = ast.literal_eval(cache_regular(str(self.file_prams_exit())))
        return multipart, params_data, self.__yaml_case

    def request_type_for_json(self, **kwargs):
        """ 判断请求类型为 json 格式 """
        _headers = self.check_headers_str_null(self.__yaml_case.headers)
        _data = self.__yaml_case.data  # dict
        _url = self.__yaml_case.url

        res = requests.request(
            method=self.__yaml_case.method,
            url=cache_regular(str(_url)),
            json=ast.literal_eval(cache_regular(str(_data))),
            data={},
            headers=_headers,
            verify=False,
            params=None,
            **kwargs
        )
        return res

    def request_type_for_none(self, **kwargs) -> object:
        """判断 requestType 为 None"""
        _headers = self.check_headers_str_null(self.__yaml_case.headers)
        _url = self.__yaml_case.url

        res = requests.request(
            method=self.__yaml_case.method,
            url=cache_regular(_url),
            data=None,
            headers=_headers,
            verify=False,
            params=None,
            **kwargs
        )
        return res

    def request_type_for_params(self, **kwargs):
        """处理 requestType 为 params """

        _data = self.__yaml_case.data
        url = self.__yaml_case.url
        if _data is not None:
            # url 拼接的方式传参
            params_data = "?"
            for key, value in _data.items():
                if value is None or value == '':
                    params_data += (key + "&")
                else:
                    params_data += (key + "=" + str(value) + "&")
            url = self.__yaml_case.url + params_data[:-1]

        _headers = self.check_headers_str_null(self.__yaml_case.headers)

        res = requests.request(
            method=self.__yaml_case.method,
            url=cache_regular(url),
            headers=_headers,
            verify=False,
            data={},
            params=None,
            **kwargs)
        return res

    def request_type_for_data(self, **kwargs):
        """
        判断 requestType 为 data 类型,且Content-Type: multipart/form-data
        :param kwargs:
        :return:
        """
        data = self.__yaml_case.data
        _headers = self.check_headers_str_null(self.__yaml_case.headers)
        _data, _headers = self.multipart_in_headers(
            ast.literal_eval(cache_regular(str(data))),
            _headers
        )
        _url = self.__yaml_case.url
        res = requests.request(
            method=self.__yaml_case.method,
            url=cache_regular(_url),
            data=_data,
            headers=_headers,
            verify=False,
            **kwargs)

        return res

    def request_type_for_file(self, **kwargs):
        """
        处理 requestType 为 file 类型，需要上传文件
        :param kwargs:
        :return:
        """
        multipart = self.upload_file()  # (MultipartEncoder对象)
        yaml_data = multipart[2]
        _headers = multipart[2].headers
        _headers = self.check_headers_str_null(_headers)
        # print('~'*50, multipart)

        res = requests.request(
            method=self.__yaml_case.method,
            url=cache_regular(yaml_data.url),
            data=multipart[0],
            params=multipart[1],
            headers=ast.literal_eval(cache_regular(str(_headers))),
            verify=False,
            **kwargs
        )
        # print('*'*50, res.request.body)
        return res

    @classmethod
    def response_elapsed_total_seconds(cls, res:Response) -> float:
        """
        获取接口响应时长
        :param res:
        :return:
        """
        try:
            return round(res.elapsed.total_seconds() * 1000, 2) # elapsed.total_seconds() 方法返回一个精确到微秒级别的时间差值
        except Exception as e:
            logging.error(e)
        finally:
            return 0.00

    def _request_body_handler(self, data: Dict, request_type: Text) -> Union[None, Dict]:
        """处理请求参数 """
        if request_type.upper() == 'PARAMS':
            return None
        else:
            return data

    def _sql_data_handler(self, sqls:Union[None, list], res: Response):
        """
        处理测试用例中，断言sql 的部分。
        :param sqls:
        :param res: 接口响应
        :return:
        """
        if config.mysql_db.switch and sqls is not None:
            sal_data = AssertSqlExecution().assert_sql_execution(
                sqls=sqls,
                resp=res.json()
            )
        else:
            sqls = {"sql": None}
        return sqls



    def _check_params(
            self,
            res: Response,
            yaml_data: "TestCase",
    ) -> "ResponseData":
        """
        组装接口的请求数据和响应数据
        :param res:
        :return:
        """
        data = ast.literal_eval(cache_regular(str(yaml_data.data)))  # 请求数据
        _organize_data = {
            "is_clear_api": yaml_data.is_clear_api,
            "url": res.url,
            "detail": yaml_data.detail,
            "response_data": res.text,
            # 这个用于日志专用，判断如果是get请求，直接打印url
            "request_body": self._request_body_handler(data, yaml_data.requestType),
            "method": res.request.method,
            "sql_data": self._sql_data_handler(
                sqls=ast.literal_eval(cache_regular(str(yaml_data.sql))),
                res=res),
            "yaml_data": yaml_data,
            "headers": res.request.headers,
            "cookie": res.cookies,
            "assert_data": yaml_data.assert_data,
            "res_time": self.response_elapsed_total_seconds(res),
            "status_code": res.status_code,
            "teardown": yaml_data.teardown,
            "teardown_sql": yaml_data.teardown_sql,
            "body": data,   # 测试用例中的请求数据
            "res_request": res.request.body     # 接口请求后的请求数据
        }

        # 抽离出通用模块，判断 http_request 方法中的一些数据校验
        return ResponseData(**_organize_data)

    def http_request(self, **kwargs):
        """ 请求封装 """

        requests_type_mapping = {
            RequestType.JSON.value: self.request_type_for_json,
            RequestType.NONE.value: self.request_type_for_none,
            RequestType.PARAMS.value: self.request_type_for_params,
            RequestType.FILE.value: self.request_type_for_file,
            RequestType.DATA.value: self.request_type_for_data
        }

        is_run = ast.literal_eval(cache_regular(str(self.__yaml_case.is_run)))

        if is_run is True or is_run is None:
            _res_data=self.__yaml_case
            try:
                res = requests_type_mapping.get(self.__yaml_case.requestType)(**kwargs)

                if self.__yaml_case.sleep is not None:
                    time.sleep(self.__yaml_case.sleep)

                _res_data = self._check_params(
                    res=res,
                    yaml_data=self.__yaml_case)
                return _res_data
            except Exception as e:
                raise e


if __name__ == '__main__':
    pass
