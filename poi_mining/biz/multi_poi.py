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
访问mongo获取POI信息
"""
import util
import json
import util
import sys

class Multi(object):
    """访问Mongo并, mkpoi返回json格式的poi信息"""

    def __init__(self):
        self.driver = __import__('pymongo')
        self.mongo = self.driver.MongoClient("10.208.248.48", 9000)
        self.db = self.mongo.multi_poi
        self.db.authenticate(name='jingpin_r', password='r_jingpin')
        self.cursor = None

    def select_by_id(self, pid):
        """按照poi-id在final表中进行查询"""
        self.cursor = self.db.final_poi.find({"firm_id":int(pid)})
        try:
            return self.cursor[0]
        except Exception as e:
            return None

    def mkpoi_by_oid_from_original(self, oid, src):
        """根据oid得到json格式的数据内容"""
        try:
            self.cursor = self.db.original_poi.find({"oid": str(oid), "src": src})
            info = self.cursor[0]
            x, y = util.coordtrans("bd09ll", "bd09mc", info['longitude'], info['latitude'])
            poi = {
              "id": int(info['oid']),
              "catalog": 0,
              "point_x": int(x),
              "point_y": int(y),
              "name": info['name'].encode("GBK"),
              "city": info['city'].encode("GBK"),
              "address": info['address'].encode("GBK"),
              "phone": info['phone'].encode("GBK")
            }
            return poi
        except Exception as e:
            #print e
            return {}

    def mkpoi_by_oid_from_source(self, oid, src):
        """根据oid得到json格式的数据内容"""
        try:
            info = self.db.source_poi.find({"oid": str(oid), "src": src})[0]
            x, y = util.coordtrans("bd09ll", "bd09mc", info['longitude'], info['latitude'])
            poi = {
              "id": info['firm_id'],
              "catalog": 0,
              "point_x": int(x),
              "point_y": int(y),
              "name": info['name'].encode("GBK"),
              "city": info['city'].encode("GBK"),
              "address": info['address'].encode("GBK"),
              "phone": info['phone'].encode("GBK")
            }
            return poi
        except Exception as e:
            return {}

    def mkpoi(self, pid):
        """根据pid得到json格式的数据内容"""
        try:
            info = self.select_by_id(pid)
            #x, y = util.coordtrans("bd09ll", "bd09mc", info['longitude'], info['latitude'])
            poi = {
              "poiId": info['firm_id'],
              "location": '%s,%s' % (str(info['longitude']), str(info['latitude'])),
              "poiName": info['name'],
              "poiCityName": info['city'],
              "address": info['address'],
              "phone": info['phone']
            }
            return poi
        except Exception as e:
            print e
            return {}

    def print_as_line2(self, oid, src, flag=None):
        """查询数据并拼接成为一行打印输出"""
        info = self.mkpoi_by_oid_from_original(oid, src)
        if info:
            if flag:
                print (u'\t'.join([flag.decode('UTF-8'),
                                   str(info['id']),
                                   info['name'],
                                   info['address'],
                                   info['city'],
                                   str(info['point_x']),
                                   str(info['point_y']),
                                   info['phone']])).encode('UTF-8')
            else:
                print (u'\t'.join([str(info['id']),
                                   info['name'].decode('GBK'),
                                   info['address'].decode('GBK'),
                                   info['city'].decode('GBK'),
                                   str(info['point_x']),
                                   str(info['point_y']),
                                   info['phone'].decode('GBK')])).encode('UTF-8')
        else:
            print "Nothing in mongo with pid=%s" % pid

    def join_by_deli(self, pid, deli=u'\t'):
        """根据给定的分隔符拼接字段"""
        info = self.select_by_id(pid)
        if info:
            return deli.join([str(info['firm_id']),
                              info['name'],
                              info['address'],
                              info['city'],
                              str(info['longitude']),
                              str(info['latitude']), info['phone']])
        else:
            return ''

    def print_as_line(self, pid, flag=None, mk=False):
        """查询并拼接打印"""
        info = self.select_by_id(pid)
        if info:
            if flag:
                if mk:
                    x, y = util.coordtrans("bd09ll", "bd09mc", info['longitude'], info['latitude'])
                    print (u'\t'.join([flag.decode('UTF-8'),
                                       str(info['firm_id']),
                                       info['name'],
                                       info['address'],
                                       info['city'],
                                       str(int(x)),
                                       str(int(y)),
                                       info['phone']])).encode('UTF-8')
                else:
                    print (u'\t'.join([flag.decode('UTF-8'),
                                       str(info['firm_id']),
                                       info['name'],
                                       info['address'],
                                       info['city'],
                                       str(info['longitude']),
                                       str(info['latitude']),
                                       info['phone']])).encode('UTF-8')
            else:
                if mk:
                    x, y = util.coordtrans("bd09ll", "bd09mc", info['longitude'], info['latitude'])
                    print (u'\t'.join([str(info['firm_id']),
                                       info['name'],
                                       info['address'],
                                       info['city'],
                                       str(int(x)),
                                       str(int(y)),
                                       info['phone']])).encode('UTF-8')
                else:
                    print (u'\t'.join([str(info['firm_id']),
                                       info['name'],
                                       info['address'],
                                       info['city'],
                                       str(info['longitude']),
                                       str(info['latitude']),
                                       info['phone']])).encode('UTF-8')
        else:
            print "Nothing in mongo with pid=%s" % pid


if __name__ == '__main__':
    multi = Multi()
    #print multi.mkpoi_by_oid_from_original(sys.argv[1], "map_life_new")
    #multi.print_as_line2(sys.argv[1], "map_life_new")
    multi.print_as_line(sys.argv[1])
