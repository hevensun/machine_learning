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
生成LogEntropy矩阵并筛选出合适的词汇
"""

import glob
import collections
import pandas
from sklearn.feature_extraction.text import CountVectorizer
import math


class LogEntropy(object):
    """计算logentropy， 得到类别关键字"""

    def __init__(self):
        self.fnames = glob.glob('data/segs/names.*')

    def extract_segs(self):
        """分词文件中获取分词结果"""
        idx = []
        words = []
        for f in self.fnames:
            lines = []
            for i, line in enumerate(open(f)):
                if i % 2 == 1:
                    non_int = '\t'.join([e for e in line.decode('GBK').rstrip('\n').split('\t') \
                            if not e.isdigit()])
                    lines.append(non_int)
            words.append('\t'.join(lines))
            idx.append(f.split('.')[1][1:])
        return words, idx

    def mk_document_term_matrix(self):
        """生成TDM矩阵"""
        words, idx = self.extract_segs()
        countvec = CountVectorizer()
        dtm = pandas.DataFrame(countvec.fit_transform(words).toarray(),
                               columns=countvec.get_feature_names(),
                               index=idx)
        """
                canting  faguo  riben  zhongwen
        1001        1      0      0         1
        991         1      0      1         0
        203         1      1      0         0
        """
        return dtm

    def global_weighting(self, dtm):
        """ 1 - Entropy(words) / log(N) """
        # normalized entropy for word
        pdtm = (dtm / dtm.sum(axis=0))
        ndocs = pdtm.shape[0]
        gw = 1 + (pdtm.applymap(lambda x: x * math.log(x) if x != 0 else 0).sum() / math.log(ndocs))
        """
        canting     2.220446e-16
        faguo       1.000000e+00
        riben       1.000000e+00
        zhongwen    1.000000e+00
        """
        return gw

    def local_weighting(self, dtm):
        """ math.log(freq + 1)"""
        lw = dtm.applymap(lambda freq: math.log(freq + 1))
        """
              canting     faguo     riben  zhongwen
        1001  0.693147  0.000000  0.000000  0.693147
        991   0.693147  0.000000  0.693147  0.000000
        203   0.693147  0.693147  0.000000  0.000000
        """
        return lw

    def logEntropyWeighting(self):
        """计算最终的logentropy得分"""
        dtm = self.mk_document_term_matrix()
        """
              canting       faguo     riben     zhongwen
        1001  1.539096e-16  0.000000  0.000000  0.693147
        991   1.539096e-16  0.000000  0.693147  0.000000
        203   1.539096e-16  0.693147  0.000000  0.000000

        """
        logEntro = (self.global_weighting(dtm.copy()) *
                    self.local_weighting(dtm)).applymap(
                            lambda x: 0 if x < 0.001 else x
                   )
        logEntro.T.to_csv('data/keyWords.cates', sep='\t', encoding='UTF-8')


if __name__ == '__main__':
    lsaEntropy = LogEntropy()
    lsaEntropy.logEntropyWeighting()
