#!/usr/bin/python
# encoding:utf-8

# ##############################################################################
# The MIT License (MIT)
#
# Copyright (c) [2015] [dangdang]
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
doc string 
"""

import traceback
import time
import util
import urllib2
import json
import sys


class RPC(object):
    """RPC request"""

    ADD_POI = 1  #新增
    CHK_POI_SINGLE = 6 #判重
    DEL_POI = 2 #删除
    CHK_POI_INNER = 5 #内部判重
    NAME_ANA = 10
    ADDR_ANA = 11
    FEATURE_ANA = 12

    def __init__(self, service_name='compute', host='127.0.0.1', port=8000):
        self.host = host
        self.port = port

    def feature_ana(self, **arg):
        """特征解析"""
        res = self._call_method(RPC.FEATURE_ANA, arg.get("detail_list", [arg]))
        return res

    def name_ana(self, **arg):
        """名称解析"""
        res = self._call_method(RPC.NAME_ANA, arg.get("detail_list", [arg]))
        return res

    def addr_ana(self, **arg):
        """地址解析"""
        res = self._call_method(RPC.ADDR_ANA, arg.get("detail_list", [arg]))
        return res

    def check_poi_inner(self, **arg):
        """内部判重"""
        res = self._call_method(RPC.CHK_POI_INNER, arg.get("detail_list", [arg]))
        return res

    def del_poi(self, **arg):
        """删除poi数据"""
        res = self._call_method(RPC.DEL_POI, arg.get("detail_list", [arg]))
        return res

    def add_poi(self, **arg):
        """增加poi数据"""
        res = self._call_method(RPC.ADD_POI, arg.get("detail_list", [arg]))
        return res

    def check_poi_single(self, **arg):
        """poi判重"""
        res = self._call_method(RPC.CHK_POI_SINGLE, arg.get("detail_list", [arg]))
        return res

    def _call_method(self, method_type, detail_list):
        """call-request"""
        url = ""
        if method_type == RPC.ADD_POI:
            url = "http://%s:%s/ComputeService/add_poi" % (self.host, self.port)
        elif method_type == RPC.DEL_POI:
            url = "http://%s:%s/ComputeService/delete_poi" % (self.host, self.port)
        elif method_type == RPC.CHK_POI_SINGLE:
            url = "http://%s:%s/ComputeService/check_poi" % (self.host, self.port)
        elif method_type == RPC.CHK_POI_INNER:
            url = "http://%s:%s/ComputeService/check_poi_inner" % (self.host, self.port)
        elif method_type == RPC.NAME_ANA:
            url = "http://%s:%s/CompareService/name_ana" % (self.host, self.port + 2)
        elif method_type == RPC.ADDR_ANA:
            url = "http://%s:%s/CompareService/addr_ana" % (self.host, self.port + 2)
        elif method_type == RPC.FEATURE_ANA:
            url = "http://%s:%s/CompareService/feature_ana" % (self.host, self.port + 2)
        else:
            return ""
        query_map = {}
        query_map["type"] = method_type
        query_map["list"] = []
        for detail in detail_list:
            query_map["list"].append(detail)
        if method_type == RPC.NAME_ANA or method_type == RPC.ADDR_ANA or \
           method_type == RPC.FEATURE_ANA:
            query_map_tmp = {}
            query_map_tmp["pack"] = query_map["list"]
            query_map = query_map_tmp
        try:
            query_json = json.dumps(query_map, ensure_ascii=False)
            res = self._send_to_remote(url, query_json)
            return res
        except Exception as e:
            print e
        return ""

    def _send_to_remote(self, url, pack):
        """post-request"""
        headers = {"Content-Type": "application/json"}
        req = urllib2.Request(url, pack, headers=headers)
        response = urllib2.urlopen(req)
        the_page = response.read()
        response.close()
        return the_page


if __name__ == "__main__":
    pass
    #rpc = RPC(host='nj03-inf-bce-waimai-m12-127.nj03.baidu.com', port=8000)
    #es = Multi()

    #poi0 = {
    #    'id'      : 54716711,
    #    'point_x' : 13515949,
    #    'point_y' : 3504194,
    #    'catalog' : 0,
    #    'name'    : u'7080'.encode('GBK'),
    #    'address' : u'宁波市慈溪市观海卫路197号(东旺家俬北10米)'.encode('GBK'),
    #    'city'    : u'宁波市'.encode('GBK'),
    #    'phone'   : u'13805822921'.encode('GBK')
    #}

    #re_map = json.loads(rpc.check_poi_single(**poi0), encoding = "gbk")
    #print "poi0: ", json.dumps(re_map, indent = 2, ensure_ascii=False)

