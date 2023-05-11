"""
#!/usr/bin/env python
# -*- coding:utf-8 -*-

@Author : Ada
@Time : 2023/4/28 11:53
@Project : ada_pytest_api_project
@File : __init__.py.py

"""
# Code starts here...
from utils import config
from utils.cache_tool.cache_control import CacheHandler, _cache_config
from utils.format_data_tool.get_excel_data_analysis import CaseData
from utils.path_tool.get_all_files_path import get_all_files
from utils.path_tool.set_path import ensure_path_sep

print('*'*30, 'test_case/__init__.py')

def write_case_process(testpath):
    """
    获取所有用例，写入用例池中
    :return:
    """
    # 循环拿到所有存放用例的文件路径
    for i in get_all_files(file_path=ensure_path_sep(testpath), excel_data_switch=True):
        # 循环读取文件中的数据
        # case_process为 list；每个元素为字典，字典的 key 为case_id；value 为对应的值
        case_process = CaseData(i).case_process(case_id_switch=True)
        if case_process is not None:
            # 转换数据类型
            for case in case_process:
                for k, v in case.items():   #k 为case_id，v 为对应的值
                    # 判断 case_id 是否已存在
                    case_id_exit = k in _cache_config.keys()
                    # 如果case_id 不存在，则将用例写入缓存池中
                    if case_id_exit is False:
                        CacheHandler.update_cache(cache_name=k, value=v)
                        # case_data[k] = v
                    # 当 case_id 为 True 存在时，则跑出异常
                    elif case_id_exit is True:
                        raise ValueError(f"case_id: {k} 存在重复项, 请修改case_id\n"
                                         f"文件路径: {i}")

write_case_process(testpath=config.want_to_create_testcase_py)

if __name__ == '__main__':
    print(_cache_config)