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

import urllib2
import json


def fetch_poi(pid):
    """访问API并得到poi数据"""
    URI = 'http://poi-relation.int.nuomi.com/poiinfo/getPoiNuomiInfo?firm_id=%s'
    response = urllib2.urlopen(URI % str(pid))
    obj = json.loads(response.read(), encoding='UTF-8')
    response.close()
    return obj


def join_by_deli(pid):
    """拼接字段为行, 输出poi信息"""
    obj = fetch_poi(pid)
    info = u'\t'.join([
                obj['data']['name'],
                str(obj['data']['firm_id']),
                obj['data']['address'],
                obj['data']['city'],
                obj['data']['phone']
           ])
    return info


def mkpoi(pid):
    """访问萌芽数据服务, 得到具体poi字段内容"""
    obj = fetch_poi(pid)
    if obj['msg'].lower() == u'success':
        return {
                "poiId": obj['data']['firm_id'],
                "address": obj['data']['address'],
                "poiCityName": obj['data']['city'],
                "location": '%s,%s' % (str(obj['data']['longitude']), str(obj['data']['latitude'])),
                'phone': obj['data']['phone'],
                'poiName': obj['data']['name']
        }
    return {}
