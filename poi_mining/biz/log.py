#!/usr/bin/env python
# encoding:utf-8

# ##############################################################################
# The MIT License (MIT)
#
# Copyright (c) [2015] [baidu.com]
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# ##############################################################################

"""
docstring for module
"""

import logging
import os
import threading
import time
from logging.handlers import TimedRotatingFileHandler


class Log(object):
    """一个遗留的老的log类"""

    instance = None
    mutex = threading.Lock()
    level = "info"
    dir = "./log"
    mode = "w"
    logFilename = time.strftime(
        '%Y%m%d', time.localtime(time.time())) + r".log"

    def __init__(self):
        self.logging = logging
        self.logger = logging.getLogger("")
        self.__level_dict = {
            'debug': logging.DEBUG,
            'info': logging.INFO,
            'warning': logging.WARNING,
            'error': logging.ERROR,
            'critical': logging.CRITICAL,
        }
        if Log.level not in self.__level_dict:
            self.logger.setLevel(logging.DEBUG)
        else:
            self.logger.setLevel(self.__level_dict[Log.level])
        filename = Log.logFilename
        if Log.dir and (not os.path.exists(Log.dir)):
            os.mkdir(Log.dir)
        if Log.dir:
            fh = TimedRotatingFileHandler(
                Log.dir + "/" + "%s" % filename, "midnight", interval=1, backupCount=10)
        else:
            fh = TimedRotatingFileHandler(
                filename, "midnight", interval=1, backupCount=10)
        fh.setLevel(self.__level_dict[Log.level])
        formatter = logging.Formatter(
            "%(asctime)s %(name)s[line:%(lineno)d] %(levelname)s %(message)s")
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)

    @staticmethod
    def get_logger(loggerName="default", dir=None, level=None, logFilename=None, mode=None):
        """get logger"""
        if(Log.instance is None):
            Log.mutex.acquire()
            if(Log.instance is None):
                if isinstance(dir, str):
                    Log.dir = dir
                if level and isinstance(level, str):
                    Log.level = level
                if logFilename and isinstance(logFilename, str):
                    Log.logFilename = logFilename
                if mode and (mode == "a" or mode == "w"):
                    Log.mode = mode
                Log.instance = Log()
            Log.mutex.release()
        return Log.instance.logging.getLogger(loggerName)


if __name__ == "__main__":
    log = Log.get_logger()
    log.info("info log")
    log.error("error log")
    log.warning("warning log")

