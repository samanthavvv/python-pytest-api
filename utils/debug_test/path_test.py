"""
#!/usr/bin/env python
# -*- coding:utf-8 -*-

@Author : Ada
@Time : 2023/4/28 11:10
@Project : ada_pytest_api_project
@File : path_test.py

"""
# Code starts here...
import ast
import json


def format_data(values: str):
    if isinstance(values, str):
        new_value = values.replace('\n', '').replace('\t', '')
        try:
            new_value = json.loads(new_value)
        except Exception as e:
            print(e)
        print(new_value)
        return new_value


v = '[{"id":"$cache {1999 _id}","updateby":null,"deleted":false,"version":0,"extData":{},"pid":"-1","brotherId":null,"parent":null,"children":[],"accountId":"$cache{acid}","subjectCode":"1999","subjectName":"1999科目","category":"资产","direct":0,"reckonMark":"N","reckonUnit":" ","active":"Y","isBuiltin":null,"isAssist":"N","isForeignCurrency":"N","isClosingExchangeRate":"N","isCashFlowItem":"N","isFooter":"Y","clientId":null,"rowIndex":null,"assistIdList":null,"customAssistIdList":null,"currencyIdList":null,"shortCode":null,"assist":null,"currency":null,"orderNo":null,"rowNum":null,"subjectCodeName":null,"cashFlowItemId":null,"currencyIsEnabled":null,"subjectNameAndAssistCategory":null,"disableUsername":null,"currencyCode":null,"currencyIds":null,"disableClick":null,"isAssistItem":null,"_level":1,"_expanded":true,"_show":true}]'
format_data(v)