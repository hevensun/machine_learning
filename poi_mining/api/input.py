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
This module provide configure file management service in i18n environment.
"""

import sys
import json

class RequestData(object):
    """
    请求数据类对象
    """
    def __init__(self):
        """
        初始化
        """
        self.aid = -1
        self.content = None
        self.debug = False
        self.city_id = None
        self.city_name = None

    def reset(self):
        """reset object status"""
        self.aid = 0
        self.content = None
        self.content = False

    def load(self, data):
        """
        将传入参数解析出来
        """
        str_res = json.loads(data)
        self.aid = str_res["globalId"]
        self.content = urllib2.unquote(str_res["content"])

    def tostr(self):
        """
        返回字符串
        """
        return "globalId=" + str(self.aid) + "&content=" + self.content

if __name__ == "__main__":
    obj = RequestData()
    obj.load("""{"content":"content","globalId":"12345"}""")
    print obj.tostr()

