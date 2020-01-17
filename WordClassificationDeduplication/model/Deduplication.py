from __future__ import division, unicode_literals

import warnings
import re
import hashlib
import logging
import numbers
import collections
import jieba
from jieba.analyse import extract_tags as extract_tags
import os

last_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
warnings.filterwarnings("ignore")


# 指定jieba的idf原始数据
# jieba.analyse.set_idf_path("../extra_dict/idf.txt.big")

def _hashfunc(x):
    return int(hashlib.md5(x).hexdigest(), 16)


class Simhash(object):

    def __init__(
            self, limit_val=20, fingersize=64, partion=3, reg=r'[\w\u4E00-\u9FFF]+', hashfunc=None):
        self.fingersize = fingersize
        self.reg = reg
        self.limit_val = limit_val

        # 分块统计
        self.partion = partion
        self.partionsize = (fingersize + 1) // (partion + 1)
        self.partionpart = [self.partionsize] * self.partion + [self.fingersize - self.partion * self.partionsize]

        if hashfunc is None:
            self.hashfunc = _hashfunc
        else:
            self.hashfunc = hashfunc

    def fingerprint(self, value):
        '''
        :param value: input_data
        :return: numbers.Integral,'#066b'
        '''
        if isinstance(value, str):
            self._build_by_text(value)
        elif isinstance(value, collections.Iterable):
            self._build_by_features(value)
        elif isinstance(value, numbers.Integral):
            self.value = value
        else:
            raise Exception('Bad parameter with type {}'.format(type(value)))
        # 输入处理，并进行64位的二进制转换
        return self.value, format(self.value, '#066b')

    def _tokenize(self, content):
        '''
        :param content: text->str
        :return: list->tuple_pair_word
                [('党的建设', 0.47331204260459014)]:[(split_param,weight)]
        '''
        content = ''.join(re.findall(self.reg, content))
        # 取代了论文中的英文滑动窗口的频率统计
        tokens = extract_tags(content, withWeight=True, allowPOS=(), topK=self.limit_val)
        return tokens

    def _build_by_text(self, content):
        return self._build_by_features(self._tokenize(content))

    def _build_by_features(self, features):
        v = [0] * self.fingersize

        # mask部分
        masks = [1 << i for i in range(self.fingersize)]

        if isinstance(features, dict):
            features = features.items()
        for f in features:
            if isinstance(f, str):
                h = self.hashfunc(f.encode('utf-8'))
                w = 1
            else:
                # [('党的建设', 0.47331204260459014),
                #  ('管党', 0.3919595902590164),
                #  ('伟大工程', 0.3771404058754098),
                #  ('伟大事业', 0.3669713918327869)]
                assert isinstance(f, collections.Iterable)
                h = self.hashfunc(f[0].encode('utf-8'))
                w = f[1]
            for i in range(self.fingersize):
                # 进行一样mask过程
                v[i] += w if h & masks[i] else -w

        # 还原对应位置上的1
        ans = 0
        for i in range(self.fingersize):
            if v[i] > 0:
                ans |= masks[i]
        self.value = ans

    @staticmethod
    def distanceObj(one, another):
        '''
        :param another: Simhash -> Object
        :return: int
        '''
        assert one.fingersize == another.fingersize
        # 统计海明距离
        x = (one.value ^ another.value) & ((1 << one.fingersize) - 1)
        ans = 0
        while x:
            ans += 1
            x &= x - 1
        return ans

    @staticmethod
    def distance(one, another, fingersize=None):
        if fingersize:
            x = (one ^ another) & ((1 << fingersize) - 1)
        else:
            x = one ^ another
        ans = 0
        while x:
            ans += 1
            x &= x - 1
        return ans

    def getsubpartions(self, value):
        subs = []
        subs_str = []
        for i, part in enumerate(self.partionpart):
            # masks值
            masks = (1 << part) - 1
            # 位移到对应模块
            sub_k = (value >> (part * i)) & masks
            subs.append(sub_k)
            subs_str.append(format(sub_k, '#018b'))

        return subs, subs_str


class IndexSimhash:
    def __init__(self, objs=None, fingersize=64, partion=3, cutoff=3):
        self.fingersize = fingersize
        self.partion = partion
        self.cutoff = cutoff

        self.partionsize = (fingersize + 1) // (partion + 1)
        self.partionpart = [self.partionsize] * partion + [fingersize - self.partionsize * partion]
        self.buckets = collections.defaultdict(set)

        if isinstance(objs, collections.Iterable):
            for obj in objs:
                self.add(*obj)

    def add(self, index, value):
        '''
        :param index: article 索引
        :param value: simhash code
        :return:
        '''
        v = "%d:%d" % (value, index)
        keys = self.getsubpartions(value)

        for key in keys:
            self.buckets[key].add(v)

    def remove(self, index, value):
        v = "%s:%s" % (value, index)
        keys = self.getsubpartions(value)
        for key in keys:
            if v in self.buckets[key]:
                self.buckets[key].remove(v)

    def get_similarity(self, value):
        keys = self.getsubpartions(value)
        ans = set()
        for key in keys:
            dumps = self.buckets[key]
            for v in dumps:
                dump_value, dump_index = v.split(':')
                if Simhash.distance(value, int(dump_value)) <= self.cutoff:
                    ans.add(dump_index)
        return list(ans)

    def getsubpartions(self, value):
        for i, part in enumerate(self.partionpart):
            masks = (1 << part) - 1
            sub_k = (value >> (part * i)) & masks
            yield "%d:%d" % (sub_k, i)


class Deduplication():
    def __init__(self, docs, type="longest", sep="\t", partion=3, cutoff=0):
        self.simhash = Simhash()
        self.indexsimhash = IndexSimhash(partion=partion, cutoff=cutoff)

        logging.basicConfig(filename=last_path + '/logging/myapp.log', level=logging.INFO, format=LOG_FORMAT)
        self.log = logging

        self.type = type
        self.sep = sep
        self.docs_dict = dict(enumerate(docs.split(sep)))
        if type not in ("longest", "newest"):
            raise TypeError
        docsE = enumerate(docs.split(sep))

        self.lendict = {}
        if docsE:
            for k, v in docsE:
                self.lendict[str(k)] = len(v)
                code, _ = self.simhash.fingerprint(v)
                self.indexsimhash.add(k, code)

        self.log.info('Initializing docs len distribution %s.', self.lendict)

    def start(self, text):
        # 新增的推荐文本id，自增
        recommend_id = str(int(max(self.lendict.keys())) + 1)
        # 长度补充
        self.lendict[recommend_id] = len(text)
        # 文本扩充
        self.docs_dict[int(recommend_id)] = text

        code, _ = self.simhash.fingerprint(text)
        ans = self.indexsimhash.get_similarity(code)
        if ans:
            self.log.info('target to %s, will delete from index:%s.', recommend_id, ans)
            ans.append(recommend_id)
            if self.type == "longest":
                top_length = 0
                for item in ans:
                    if self.lendict.get(str(item), 0) > top_length:
                        top_length = self.lendict.get(str(item))
                        recommend_id = item
            for item in ans:
                if item != recommend_id:
                    self.lendict[item] = 0
                    text = self.docs_dict.pop(int(item))
                    code, _ = self.simhash.fingerprint(text)
                    self.indexsimhash.remove(int(item), code)
        self.indexsimhash.add(int(recommend_id), code)
        self.log.info('target to %s, will add index:%s.', recommend_id, recommend_id)

        self.log.info('target to %s, Now docs maintain index:%s.', recommend_id, self.docs_dict)
        return recommend_id, ans