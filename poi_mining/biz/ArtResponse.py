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
ArtResopnse & ArtRequest
"""


class ArtRequest(object):
    """文章基本的解析结果"""

    def __init__(self, js):
        pass


class ArtResponse(object):
    """Response对象, 用于保存主要response数据"""

    def __init__(self, aid, mkpoi, debug=False):
        self.debuginfo = []
        self.mypois = {}
        self.pids = []
        self.all_addresses = []
        self.all_names = []
        self.city = None
        self.aid = aid
        self.debug = debug
        self.mkpoi = mkpoi

    def toKeyValue(self):
        """对象转化为dict"""
        if self.debug:
            return {
                'poiDetail': self.mypois,
                'poiList': self.pids,
                'poiInfo': [self.mkpoi.join_by_deli(_id) for _id in self.pids],
                'poiNum': len(self.pids),
                'debuginfo': self.debuginfo,
                'artid': self.aid,
                'city': self.city,
                'address': self.all_addresses,
                'names': self.all_names
            }
        return {
            'poiDetail': self.mypois,
            'poiList': self.pids,
            'poiNum': len(self.pids)
        }


