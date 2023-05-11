"""
#!/usr/bin/env python
# -*- coding:utf-8 -*-

@Author : Ada
@Time : 2023/5/4 10:36
@Project : ada_pytest_api_project
@File : regular_control.py

"""
# Code starts here...
import logging
import random
import re
import time
from datetime import datetime
from faker import Faker
from jsonpath import jsonpath
from utils import config
from utils.cache_tool.cache_control import CacheHandler
from utils.logging_tool.log_control import ERROR

logging.getLogger('faker').setLevel(logging.ERROR)

class Context:
    def __init__(self):
        self.faker = Faker(locale='zh_CN')

    @classmethod
    def random_int(cls) -> int:
        """
        :return: 随机数
        """
        _data = random.randint(0, 5000)
        return _data

    def get_phone(self) -> int:
        """
        :return: 随机生成手机号码
        """
        phone = self.faker.phone_number()
        return phone


    def get_id_number(self) -> int:
        """

        :return: 随机生成身份证号码
        """

        id_number = self.faker.ssn()
        return id_number

    def get_female_name(self) -> str:
        """

        :return: 女生姓名
        """
        female_name = self.faker.name_female()
        return female_name

    def get_male_name(self) -> str:
        """

        :return: 男生姓名
        """
        male_name = self.faker.name_male()
        return male_name

    def get_email(self) -> str:
        """

        :return: 生成邮箱
        """
        email = self.faker.email()
        return email

    @classmethod
    def get_time(cls) -> str:
        """
        计算当前时间
        :return:
        """
        now_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return now_time

    @classmethod
    def get_now_time(cls) -> int:
        """
        计算当前时间的时间戳
        :return: 返回一个13位的时间戳
        """
        return round(time.time()*1000)  #1694609388318

    @classmethod
    def host(cls) -> str:
        from utils import config
        """ 获取接口域名 """
        return config.host

    @classmethod
    def app_host(cls) -> str:
        from utils import config
        """获取app的host"""
        return config.app_host

    @classmethod
    def get_acid(cls):
        # todo 获取账套id
        acids = CacheHandler.get_cache('acids')
        _acid = jsonpath(acids, f'$.[*][?(@.accountCode=="{config.account_code}")].id')[0]
        return _acid

    @classmethod
    def create_name_or_id(cls, name: str = '名'):
        return name + str(cls.get_now_time())

def sql_json(js_path, res):
    """ 提取 sql中的 json 数据 """
    _json_data = jsonpath(res, js_path)[0]
    if _json_data is False:
        raise ValueError(f"sql中的jsonpath获取失败 {res}, {js_path}")
    return jsonpath(res, js_path)[0]

def sql_regular(value, res=None):
    """
    这里处理sql中的依赖数据，通过获取接口响应的jsonpath的值进行替换
    :param res: jsonpath使用的返回结果
    :param value: 例如：value=select xxx from users where id=$json($.data[0].applyId)$
    :return:
    """
    sql_json_list = re.findall(r"\$json\((.*?)\)\$", value)  # $json($.data[0].applyId)$

    for i in sql_json_list:
        # pattern = '\\$json\\(select xxx from users where id=\\$json(\\$.data\\[0].applyId)\\$\\)\\$'
        pattern = re.compile(r'\$json\(' + i.replace('$', "\$").replace('[', '\[') + r'\)\$')
        key = str(sql_json(i, res))
        value = re.sub(pattern, key, value, count=1)

    return value

def cache_regular(value):
    """
    使用正则替换测试用例中的数据。数据源来于从缓存中读取，一般是测试执行过程中，存到缓存中的。
    :param value:
    :return:
    """
    pattern = r'\$cache{(.*?)}'
    regex = re.compile(pattern)
    regular_datas = regex.findall(value)    # list.所有匹配到的数据

    for regular_data in regular_datas:
        value_types = ['int:', 'bool:', 'list:', 'dict:', 'tuple:', 'float:']
        try:
            if any(i in regular_data for i in value_types) is True:
                value_types = regular_data.split(":")[0]  # 例如，regular_data为 $cache{int:random_int()}，value_types=int，regular_type=random_int()
                regular_data = regular_data.split(":")[1]
                # todo
                # pattern = re.compile(r'\'\$cache\{' + value_types.split(":")[0] + ":" + regular_data + r'\}\'')
            else:
                # todo
                pattern = re.compile(r'\$cache{' + regular_data + r'}')
            cache_data = CacheHandler.get_cache(regular_data)
            value = re.sub(pattern, str(cache_data), value)
        except AttributeError:
            ERROR.logger.error("未找到对应的替换的数据, 请检查数据是否正确 %s", value)
        except IndexError:
            ERROR.logger.error("测试用例中的 $cache{} 函数方法不正确，正确语法实例：$cache{login_int}")
            raise
    return value

def regular(target):
    """
    使用正则替换测试用例中的数据。数据源来于从配置文件中读取，或者通过 faker 等制造的测试数据。
    :param target:
    :return:
    """
    try:
        regular_pattern = r'\${{(.*?)}}'
        while re.findall(regular_pattern, target):
            key = re.search(regular_pattern, target).group(1)
            value_types = ['int:', 'bool:', 'list:', 'dict:', 'tuple:', 'float:']
            if any(i in key for i in value_types) is True:
                # 当处理完的数据需要进行特定格式转换时
                # TODO 暂时想不到使用场景
                pass
            else:
                func_name = key.split("(")[0]
                value_name = key.split("(")[1][:-1]
                if value_name == "":
                    #当无参数时
                    value_data = getattr(Context, func_name)()
                else:
                    # 当有参数时,目前只适用于位置参数
                    value_data = getattr(Context, func_name)(*value_name.split(","))
                target = re.sub(regular_pattern, str(value_data), target, 1)
        return target
    except AttributeError:
        print("未找到对应的替换的数据, 请检查数据是否正确 %s", target)
    except IndexError:
        print("yaml中的 ${{}} 函数方法不正确，正确语法实例：${{get_time()}}")
        raise




if __name__ == '__main__':
    CacheHandler.update_cache(cache_name='authorization', value='12345')
    CacheHandler.update_cache(cache_name='login_int', value='123456')
    a = "$cache{authorization},fdasfsffs $cache{login_int}"
    cache_regular(a)
    print(a)
    # d = "assistCode: ${{create_name_or_id(gys-)}}, ${{host()}}"
    # r = regular(d)
    # print(r)