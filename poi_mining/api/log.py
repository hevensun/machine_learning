#coding:utf-8
################################################################################
#
### Copyright (c) 2015 Baidu.com, Inc. All Rights Reserved
#
##################################################################################
"""
This module provide configure file management service in i18n environment.

Authors: wangdia01(wangdian01@baidu.com)
Date:    2015/07/14
"""

import os
import logging
import logging.handlers

class EasyLog(object):
    """
    the log class
    """
    def __init__(self):
        """
        the init function
        """
        self.logger = logging.getLogger()

    def init_log(self, log_path, level=logging.INFO, when="D", backup=7,
        format="%(levelname)s: %(asctime)s: %(filename)s:%(lineno)d * %(thread)d %(message)s",
        datefmt="%m-%d %H:%M:%S"):
        """
        init_log - initialize log module
        Args:
          log_path      - Log file path prefix.
                          Log data will go to two files: log_path.log and log_path.log.wf
                          Any non-exist parent directories will be created automatically
          level         - msg above the level will be displayed
                          DEBUG < INFO < WARNING < ERROR < CRITICAL
                          the default value is logging.INFO
          when          - how to split the log file by time interval
                              'S' : Seconds
                              'M' : Minutes
                              'H' : Hours
                              'D' : Days
                              'W' : Week day
                              default value: 'D'
          format        - format of the log
                          default format:
                          %(levelname)s: %(asctime)s: %(filename)s:%(lineno)d * %(thread)d %(message)s
                          INFO: 12-09 18:02:42: log.py:40 * 139814749787872 HELLO WORLD
          backup        - how many backup file to keep
                          default value: 7
       Raises:
              OSError: fail to create log directories
              IOError: fail to open log file
        """
        formatter = logging.Formatter(format, datefmt)
        self.logger.setLevel(level)
        dir = os.path.dirname(log_path)
        if not os.path.isdir(dir):
            os.makedirs(dir)
        handler = logging.handlers.RotatingFileHandler(log_path + ".log",
        maxBytes = 10 * 1024 * 1024,
        backupCount = backup)
        handler.setLevel(level)
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        handler = logging.handlers.RotatingFileHandler(log_path + ".log.wf",
        maxBytes = 10 * 1024 * 1024,
        backupCount = backup)
        handler.setLevel(logging.WARNING)
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def info(self, msg):
        """write the info message to the log file
        """
        return self.logger.info(msg)

    def debug(self, msg):
        """write the debug message to the log file
        """
        return self.logger.debug(msg)

    def warn(self, msg):
        """write the warnning message to the log file
        """
        return self.logger.warning(msg)

    def error(self, msg):
        """write the error message to the log file
        """
        return self.logger.error(msg)

    def monitor(self, msg):
        """write the monitor message to the log file
        """
        monitor_msg = "[Monitor]" + msg
        return self.logger.info(monitor_msg)


if __name__ == '__main__':
    mylog = EasyLog()
    mylog.init_log("../logs/test.log")
    mylog.info('Hello World!')
    mylog.warn('Warning')
