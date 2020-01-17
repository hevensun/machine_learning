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
import collections
import copy

class CityGeoTree(object):
    """predict city of articles"""

    def __init__(self, city_tree_file):
        self.word2parent = {}
        self.id2word = {}
        self.words = set()
        self.word2level = {}

        for line in open(city_tree_file,encoding='GBK'):
            fields = line.rstrip('\n').split('\t')
            # words只有2，3，4级别的地名
            if int(fields[3]) == 2 or int(fields[3]) == 3 or int(fields[3]) == 4:
                self.words.add(fields[1])

            # 地名对应的级别
            self.word2level[fields[1]] = int(fields[3])

            # word2parent，地名对应的上级地名的id
            if fields[1] in self.word2parent:
                self.word2parent[fields[1]].append(int(fields[2]))
            else:
                self.word2parent[fields[1]] = [int(fields[2])]

            # 唯一id对应的地名
            self.id2word[int(fields[0])] = fields[1]

    def clean(self, word):
        """清理后缀"""
        return word.replace(u'地区', '').replace(u'省', '')\
                .replace(u'市', '').replace(u'自治区', '')\
                .replace(u'特别行政区', '')

    def chain(self, c, tolevel):
        """计算地址之间的层级关系， 将3级地址匹配数汇总到2级地址"""
        oc = collections.Counter()
        for each in c:
            # 父级地址
            pids = self.word2parent[each]
            pwords = [self.id2word[pid] for pid in pids]

            # 如果需要识别的地址比汇总地址要高，则直接把原分带过来不做删减
            if self.word2level[each] <= tolevel:
                oc.update({each: c[each]})

            # 匹配级别为目标级别，其一级父级在匹配列表里面则加2，否则加1
            for pword in pwords:
                if self.word2level[each] == tolevel + 1 and \
                   self.word2level[pword] == tolevel:
                    if pword not in c:
                        oc.update({pword:c[each]/2})
                    else:
                        oc.update({pword:c[each]})
        #print json.dumps(oc, ensure_ascii=False, encoding='UTF-8', indent=2)
        return oc

    def predict(self, segs):
        """预测城市"""
        c = collections.Counter()

        # c中，直接匹配出来的为2，间接匹配(市/区匹配)出来的为1
        for each in segs:
            if each and len(each) >= 2:
                #cnword = self.clean(each)
                shi = each + u'市'
                qu = each + u'区'
                if len(each) >= 2:
                    if (each in self.words):
                        c.update([each])
                    if (shi in self.words):
                        c.update([shi])
                    if (qu in self.words):
                        c.update([qu])
                    if each[:3] in self.words:
                        c.update([each[:3]])
        #print json.dumps(c, ensure_ascii=False, encoding='UTF-8', indent=2)
        if len(c):
            c = self.chain(self.chain(c, 3), 2)
            citys = c.most_common(3)
            if citys:
                return citys[0][0]
        return None

if __name__ == '__main__':
    pred = CityGeoTree('place.txt')
    #l = [1]
    #for i, l in enumerate(open('/home/liangchengming/research/article_of_poi/planB/cases/x.gbk.seg')):
    ##print pred.predict(l.decode('GBK').split('\t')[2:])
    #    if i % 1 == 0:
    #        fields = l.decode('GBK').split('\t')
    #        if fields[0] == u'101225593504469924':
    #            print 'in'
    #            print pred.predict(fields[2:])[0].encode('UTF-8')



