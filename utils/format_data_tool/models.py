"""
#!/usr/bin/env python
# -*- coding:utf-8 -*-

@Author : Ada
@Time : 2023/4/27 15:51
@Project : ada_pytest_api_project
@File : models.py

"""
# Code starts here...
import types
from enum import Enum
from typing import Text, Union, Optional, List, Any, Dict, Callable

from pydantic import BaseModel

class MySQLdb(BaseModel):
    switch: bool = False
    host: Union[Text, None] = None
    user: Union[Text, None] = None
    password: Union[Text, None] = None
    port: Union[int, None] = 3306


class Config(BaseModel):
    want_to_create_testcase_py: Text = '\data\YunKuaiJi'  # 默认值
    host: Text
    app_host: Union[Text, None]
    mysql_db: "MySQLdb"
    account_code: Text
    current_user: Dict



class TestCaseEnum(Enum):
    """
    枚举一个测试用例（本框架中，即一个api 接口）的必须字段和非必须字段。
    对于用excel存储测试用例来说，此模型用不到。
    """

    FEATURE = ("feature", False)             # 该测试用例属于哪个业务链.颗粒度是sheet
    NAME = ("api_name", False)               # 该测试用例的名称。颗粒度是个api
    DESCRIPTION = ("description", False)     # 该测试用例的描述。颗粒度是个api
    CASE_ID = ("case_id", False)
    PARENT_CASE = ("parent_case", True)   # 该api 是否是一个用于清理工作的api
    HOST = ("host", True)
    URL = ("url", True)
    METHOD = ("method", True)
    DETAIL = ("detail", True)
    IS_RUN = ("is_run", True)
    HEADERS = ("headers", True)
    REQUEST_TYPE = ("requestType", True)
    DATA = ("data", True)
    DE_CASE = ("dependence_case", True)
    DE_CASE_DATA = ("dependence_case_data", True)
    ASSERT_DATA = ("assert", True)
    SQL = ("sql", True)                         # 用于数据库断言
    SETUP_SQL = ("setup_sql", True)             # 用于前置sql
    CURRENT_RE_SET_CACHE = ("current_request_set_cache", True)
    TEARDOWN = ("teardown", True)
    TEARDOWN_SQL = ("teardown_sql", True)       # 用于后置sql
    SLEEP = ("sleep", True)



class DependentData(BaseModel):
    """
    数据依赖详细信息。大类上区分：cache，request，response
    """
    dependent_type: Text    # 区分提取数据的数据源
    jsonpath: Text          # jsonpath 表达式
    set_cache: Optional[Text]       # 存入缓存时所用的名称。依赖和被依赖接口的关联名称
    replace_key: Optional[Text]     # 存入缓存是所用的名称


class DependentCaseData(BaseModel):
    """
    数据依赖信息。
    """

    case_id: Text  # 依赖的接口的case_id
    # dependent_data: List[DependentData]
    dependent_data: Union[None, List[DependentData]] = None  # 要从依赖接口中提取的数据及方式


class ParamPrepare(BaseModel):
    """
    后置处理中，只需要从当前的用例的响应或者请求内容中，获取数据。
    """

    dependent_type: Text
    jsonpath: Text
    set_cache: Text

class SendRequest(BaseModel):
    """
    后置处理中，当前用例A，后置接口B，需要用例B 先发送请求，再获取数据
    """

    dependent_type: Text
    jsonpath: Optional[Text]
    cache_data: Optional[Text]
    set_cache: Optional[Text]
    replace_key: Optional[Text]

class TearDown(BaseModel):
    """
    后置处理信息。大类上区分：sql，api
    """
    case_id: Text
    param_prepare: Optional[List["ParamPrepare"]]
    send_request: Optional[List["SendRequest"]]


class CurrentRequestSetCache(BaseModel):
    """
    当前接口的请求数据中，有数据需要存到缓存中时。
    """
    type: Text
    jsonpath: Text
    name: Text


class TestCase(BaseModel):
    parent_case: Union[Text, None]
    url: Text
    method: Text
    detail: Text
    is_run: Union[None, bool, Text] = None
    headers: Union[None, Dict, Text] = {}
    requestType: Text
    data: Any = None
    dependence_case: Union[None, bool] = False
    dependence_case_data: Optional[Union[None, List["DependentCaseData"], Text]] = None
    assert_data: Union[Dict, Text]
    sql: List = None
    setup_sql: List = None
    current_request_set_cache: Optional[List["CurrentRequestSetCache"]]
    teardown: Union[List["TearDown"], None] = None
    teardown_sql: Optional[List] = None
    sleep: Optional[Union[int, float]]

class Method(Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"
    HEAD = "HEAD"
    OPTION = "OPTION"

class RequestType(Enum):
    """
    request请求发送，请求参数的数据类型
    """
    JSON = "JSON"
    PARAMS = "PARAMS"
    DATA = "DATA"
    FILE = 'FILE'
    EXPORT = "EXPORT"
    NONE = "NONE"

class ResponseData(BaseModel):
    parent_case: Union[Text,None]
    url: Text
    is_run: Union[None, bool, Text]
    detail: Text
    response_data: Text
    request_body: Any
    method: Text
    sql_data: Dict
    yaml_data: "TestCase"
    headers: Dict
    cookie: Dict
    assert_data: Dict
    res_time: Union[int, float]
    status_code: int
    teardown: List["TearDown"] = None
    teardown_sql: Union[None, List]
    body: Any
    res_request: Any

class Assert(BaseModel):
    jsonpath: Text
    type: Text
    value: Any
    AssertType: Union[None, Text] = None

class AssertMethod(Enum):
    """ 断言类型 """
    equals = "=="
    less_than = "lt"
    less_than_or_equals = "le"
    greater_than = "gt"
    greater_than_or_equals = "ge"
    not_equals = "not_eq"
    string_equals = "str_eq"
    length_equals = "len_eq"
    length_greater_than = "len_gt"
    length_greater_than_or_equals = 'len_ge'
    length_less_than = "len_lt"
    length_less_than_or_equals = 'len_le'
    contains = "contains"
    contained_by = 'contained_by'
    startswith = 'startswith'
    endswith = 'endswith'

def load_module_functions(module) -> Dict[Text, Callable]:
    module_functions = {}

    for name, item in vars(module).items():  # vars() 函数返回对象object的属性和属性值的字典对象。
        if isinstance(item, types.FunctionType):
            module_functions[name] = item
    return module_functions

if __name__ == '__main__':
    d={'jsonpath': '$.success', 'type': '==', 'value': True, 'AssertType': None}
    ass = Assert(**d)
    print(ass.dict().keys())
