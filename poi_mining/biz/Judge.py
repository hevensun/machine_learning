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

import biz.ngrams


class Judge(object):
    """文章句子可用性判定"""

    def __init__(self, refuse, addr_accept, name_accept, name_suffix, skip):
        self._refuse_key = self.load_into_set(refuse)
        self._addr_accept_key = self.load_into_set(addr_accept)
        self._name_accept_key = self.load_into_set(name_accept)
        self._name_suffix = self.load_into_set(name_suffix)
        self._skip_key = self.load_into_set(skip)

    def load_into_set(self, fname):
        """加载字典"""
        ks = set()
        for line in open(fname):
            v = line.decode('UTF-8').rstrip('\n')
            if v:
                ks.add(v)
        return ks

    def refuse(self, ustring):
        """是否拒绝此句子"""
        for k in self._refuse_key:
            if k in ustring:
                return True
        return False

    def suffix_accept(self, ustring):
        """全匹配logEntropy关键词"""
        for k in self._name_suffix:
            if k in ustring:
                return True, k
        return False, None

    def name_accept(self, ustring, full=False):
        """是否接受此句子为潜在的POI名称"""
        tris = biz.ngrams.ngrams(ustring, 3)
        if full:
            if tris[0] in self._name_accept_key and tris[-1] in self._name_accept_key:
                return True
            return False
        for each in tris:
            if each in self._name_accept_key:
                return True
        return False

    def name_gram(self, gram):
        """判断给定的gram是否包含在词典中"""
        return gram in self._name_accept_key

    def addr_accept(self, ustring):
        """是否接受此句子为潜在的POI地址"""
        for k in self._addr_accept_key:
            if k in ustring:
                return True
        return False

    def skip(self, ustring):
        """是否跳过此句子的处理"""
        for k in self._skip_key:
            if k in ustring:
                return True
        return False
