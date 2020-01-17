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
1. 搜索TrieTree 得到poi名称
2. 合并搜索结果, 并去重/合并
"""

import json
import requests

class Trie(object):
    """访问Trie树索引, 匹配句子中出现的所有poi合法名称并合并去重"""

    def __init__(self, host, port):
        assert str(port).isdigit(), "Invalid port %s" % port
        self.uri = "http://%s:%s/parse_sentences" % (host, port)

    def trie_search_of_poinames(self, sent, _city):
        """搜索POI名称并做基本去重"""
        _names = []
        for s in sent:
            data = {
                'sentences': json.dumps([s.str()]).encode('UTF-8'),
                "city": _city.encode('UTF-8')
            }
            res = requests.post(self.uri, data=data).json()
            if res['info'] == 'success':
                _names.extend([(e, s.idx) for e in set(res['data'])])
        idx2names = {}
        unique_names = []
        for each in _names:
            if each[1] in idx2names and each[0] in idx2names[each[1]]:
                continue
            else:
                if each[1] in idx2names:
                    idx2names[each[1]].add(each[0])
                else:
                    idx2names[each[1]] = set([each[0]])
                unique_names.append(each)
        return sorted(unique_names, key=lambda x:len(x[0]), reverse=False)

    def search(self, sent, _city):
        """搜索POI名字, 并根据同offset内部做POI名称后缀合并"""
        unique_names = self.trie_search_of_poinames(sent, _city)
        merged_names = []
        for i in xrange(len(unique_names)):
            sub = False
            for j in xrange(i + 1, len(unique_names)):
                if unique_names[i][0] in unique_names[j][0] and \
                   unique_names[i][1] == unique_names[j][1]:
                    sub = True
                    break
            if not sub:
                merged_names.append(unique_names[i])
        return merged_names





