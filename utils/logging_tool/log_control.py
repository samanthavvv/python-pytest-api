"""
#!/usr/bin/env python
# -*- coding:utf-8 -*-

@Author : Ada
@Time : 2023/5/9 11:30
@Project : ada_pytest_api_project
@File : log_control.py

"""
# Code starts here...
import logging
import time
from logging import handlers
from typing import Text
import colorlog

from utils import ensure_path_sep


class LogHandler:
    """
    日志打印封装：handler，颜色，级别，内容
    """

    # 日志级别关系映射
    level_relations = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'critical': logging.CRITICAL
    }

    def __init__(
            self,
            filename: Text,
            level: Text = "info",
            when: Text = "D",
            fmt: Text = "%(levelname)s - %(asctime)s - %(name)s:%(filename)s:%(lineno)d %(message)s"
    ):
        self.logger = logging.getLogger(filename)
        # 设置日志级别
        self.logger.setLevel(self.level_relations.get(level))
        # 设置日志格式
        format_str = logging.Formatter(fmt)

        # 设置控制台日志
        formatter = self.log_color()
        screen_output = logging.StreamHandler()
        screen_output.setFormatter(formatter)

        # 设置文件日志
        # 添加定时更新日志handler
        """
            #实例化TimedRotatingFileHandler
            # filename：日志文件名
            # when：日志文件按什么切分。'S'-秒；'M'-分钟；'H'-小时；'D'-天；'W'-周
            #       这里需要注意，如果选择 D-天，那么这个不是严格意义上的'天'，是从你
            #       项目启动开始，过了24小时，才会重新创建一个新的日志文件，如果项目重启，
            #       这个时间就会重置。选择'MIDNIGHT'-是指过了凌晨12点，就会创建新的日志
            # interval是时间间隔
            # backupCount：是保留日志个数。默认的0是不会自动删除掉日志。如果超过这个个数，就会自动删除  
        """
        time_rotating = handlers.TimedRotatingFileHandler(
            filename=filename,
            when=when,
            backupCount=3,
            encoding="utf-8"
        )
        # file_format_str = time_rotating.setFormatter(self.log_color()) # logging.Formatter(fmt)
        time_rotating.setFormatter(format_str)

        # 把对象加到logger里
        self.logger.addHandler(screen_output)
        self.logger.addHandler(time_rotating)

    @classmethod
    def log_color(cls):
        """
        设置日志颜色和格式，用于输出到控制台的格式
        :return:
        """
        log_colors_config = {
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red',
        }

        formatter = colorlog.ColoredFormatter(
            '\n%(log_color)s[%(asctime)s] [%(name)s] [%(levelname)s]: %(message)s',
            log_colors=log_colors_config
        )
        return formatter


now_time_day = time.strftime("%Y-%m-%d", time.localtime())
INFO = LogHandler(filename=ensure_path_sep(f'/logs/info-{now_time_day}.log'), level='info')
ERROR = LogHandler(filename=ensure_path_sep(f'/logs/error-{now_time_day}.log'), level='error')
WARNING = LogHandler(filename=ensure_path_sep(f'/logs/warning-{now_time_day}.log'), level='warning')

if __name__ == '__main__':
    INFO.logger.info('测试')
    ERROR.logger.error('测试')
    WARNING.logger.warning('测试')
