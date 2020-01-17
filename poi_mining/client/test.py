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

import json
import urllib2
import urllib


def send_to_remote(url, pack):
    headers = {"Content-Type": "application/x-www-form-urlencoded ", 'charset':'UTF-8'}
    req = urllib2.Request(url, pack, headers=headers)
    response = urllib2.urlopen(req)
    the_page = response.read()
    response.close()
    return the_page


N = 0
def parse(art, x):
    """parse解析数据debug结果"""
    global N
    #id2st = {}
    #for i, each in enumerate(x):
    #    if each['type'] == 'text':
    #        id2st[i] = each['data']
    print art
    #js = json.loads(art, encoding='UTF-8')
    #print "aid:", js['data']['artid']
    #print "poiList", js['data']['poiList']
    #print "poiNum", len(js['data']['poiList'])
    #N += len(js['data']['poiList'])
    #print json.dumps(js['data']['debuginfo'], encoding='UTF-8',
    #        ensure_ascii=False, indent=2).encode('UTF-8')
    #for each in js['data']['debuginfo']:
    #    print
    #    print each[2].encode('UTF-8'), '#', each[3].encode('UTF-8')
    #    print each[1], id2st[each[1]].encode('UTF-8')
    #    print each[0], id2st[each[0]].encode('UTF-8')
    ##print len(js['data']['debuginfo'])
    #for each in js['data']['sentence']:
    #    print each.encode('UTF-8')
    #for each in js['data']['poiInfo']:
    #    print each.encode('UTF-8')


for i, line in enumerate(open('online.txt')):
    if i == 99:
        continue
    fields = line.rstrip('\n').split('\x01')
    x = urllib2.quote(fields[2])
    pay = urllib.urlencode({'globalId':int(fields[0]), 'content': x})
    url = 'http://127.0.0.1:8881/feed/poiRecognize'
    #pay = urllib.urlencode({'globalId':int(fields[0]), 'content': x, 'debug':True})
    #print json.dumps(json.loads(send_to_remote(url, pay), encoding='UTF-8'), ensure_ascii=False, indent=2).encode('UTF-8')
    print send_to_remote(url, pay)
    if i > 100:
        break


