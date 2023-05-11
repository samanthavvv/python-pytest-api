"""
#!/usr/bin/env python
# -*- coding:utf-8 -*-

@Author : Ada
@Time : 2023/5/8 13:59
@Project : ada_pytest_api_project
@File : mysql_control.py

"""
# Code starts here...
import datetime
import decimal
import logging
from typing import Text

import pymysql
from requests import Response

from utils import config
from utils.exception_tool.exceptions import DataAcquisitionFailed, ValueTypeError
from utils.regular_tool.regular_control import sql_regular

FORMAT = '%(asctime)s %(message)s'

logging.basicConfig(format=FORMAT, level=logging.DEBUG)

class MySqlDb:
    """
    处理数据库连接和关闭：上下文
    """
    def __init__(self):
        # 建立数据库连接
        self._conn = pymysql.Connect(
            host=config.mysql_db.host,
            port=config.mysql_db.port,
            user=config.mysql_db.user,
            password=config.mysql_db.password,
        )

    @property
    def conn(self):
        return self._conn

    def close_conn(self):
        try:
            if self.conn:
                self.conn.close()
        except AttributeError as error:
            logging.error("数据库连接失败，失败原因 %s", error)


    def query(self, sql, state="all"):
        """
        查询sql
        :param sql:
        :param state:
        :return:
        """
        try:
            if state == "all":
                # 查询全部
                with self.conn.cursor() as cur:
                    data = cur.fetchall()
            else:
                # 查询单条
                with self.conn.cursor() as cur:
                    data = cur.fetchone()
            return data
        except AttributeError as error_data:
            logging.error("数据库连接失败，失败原因 %s", error_data)
            raise

    def execute(self, sql: Text):
        """
            更新 、 删除、 新增
            :param sql:
            :return:
        """
        try:
            # 使用 execute 操作 sql
            with self.conn.cursor() as cur:
                rows =cur.execute(sql)
                # 提交事务
                self.conn.commit()
                return rows
        except AttributeError as error:
            logging.error("数据库连接失败，失败原因 %s", error)
            # 如果事务异常，则回滚数据
            self.conn.rollback()
            raise

    @classmethod
    def sql_data_handler(cls, query_data, data):
        """
        处理部分类型sql查询出来的数据格式
        @param query_data: 查询出来的sql数据
        @param data: 数据池
        @return:
        """
        # 将sql 返回的所有内容全部放入对象中
        for key, value in query_data.items():
            if isinstance(value, decimal.Decimal):
                data[key] = float(value)
            elif isinstance(value, datetime.datetime):
                data[key] = str(value)
            else:
                data[key] = value
        return data


class AssertSqlExecution(MySqlDb):
    def assert_sql_execution(self, sqls: list, resp: Response) -> dict:
        try:
            if isinstance(sqls, list):
                data = {}
                _sql_type = ['UPDATE', 'update', 'DELETE', 'delete', 'INSERT', 'insert']
                if any(type in sqls for type in _sql_type) is False:
                    for sql in sqls:
                        # 如果测试用例的sql 语句中有正则，需要从接口响应内容中提取数据进行替换时
                        sql = sql_regular(sql, resp)
                        if sql is not None:
                            # for 循环逐条处理断言 sql
                            query_data = self.query(sql)[0]
                            data = self.sql_data_handler(query_data, data)
                else:
                    raise DataAcquisitionFailed("断言的 sql 必须是查询的 sql")
            else:
                raise ValueTypeError("sql数据类型不正确，接受的是list")
            return data
        except Exception as e:
            logging.error(e)


if __name__ == '__main__':
    conn = MySqlDb().conn
    with conn.cursor() as cur:
        query_sql = "SELECT * FROM `zz_test`.`base_assist` WHERE `ACCOUNT_ID` = '73B3287231094B45A9989688045A47D3' LIMIT 0,1000"
        cur.execute(query_sql)
        print(cur.fetchall())
    conn.close()


