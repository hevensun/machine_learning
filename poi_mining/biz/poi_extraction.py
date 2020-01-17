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
抽取文章中门店标题和地址电话
"""

import sys
import os
import json
import unicode_utils as uni
import itertools as it
import copy
import requests
from multiprocessing.dummy import Pool as ThreadPool

sys.path.append('../')
import biz.balance
import biz.util as util
import biz.GEO_TREE.city_predict as citypred
import biz.ngrams
import biz.mkpoi as mkpoi
import biz.Judge as Judge
import biz.trie_search as Trie
from biz.ArtResponse import ArtResponse as ArtResponse


class Segmentor(object):
    """nlpc分词工具"""

    @staticmethod
    def get_term_pos(_property):
        """获取下标"""
        return ((_property) & 0x00ffffff)

    @staticmethod
    def get_term_len(_property):
        """获取长度"""
        return ((_property) >> 24)

    def __init__(self):
        sofa.use('drpc.ver_1_0_0', 'S')
        sofa.use('nlpc.ver_1_0_0', 'wordseg')
        conf = sofa.Config()
        conf.load('config/drpc_client.xml')
        self.wordseg_agent = S.ClientAgent(conf['sofa.service.nlpc_wordseg_3016'])

    def seg(self, line, cmd=0x4):
        """分词"""
        if len(line) <= 0:
            return ''
        m_input = wordseg.wordseg_input()
        m_input.query, m_input.lang_id, m_input.lang_para = str(line), 0, 0
        for i in range(5):
            try:
                ret, output_data = self.wordseg_agent.call_method(sofa.serialize(m_input))
                break
            except Exception as e:
                return ''
        if len(output_data) == 0:
            return ''

        m_output = sofa.deserialize(output_data, type(wordseg.wordseg_output())).scw_out

        # extract words from results
        if cmd & 0x4:
            _segs = []
            for i in range(m_output.wsbtermcount):
                posidx = Segmentor.get_term_pos(m_output.wsbtermpos[i])
                poslen = Segmentor.get_term_len(m_output.wsbtermpos[i])
                word = m_output.wordsepbuf[posidx:posidx + poslen]
                w = word.decode('GBK', 'ignore')
                _segs.append(w)
            return _segs


class POI(object):
    """poi对象"""

    def __init__(self):
        self.name = ""
        self.city = ""
        self.blon = 0.0
        self.blat = 0.0
        self.phone = ""
        self.address = ""
        self.offset = -1

    def reset(self, city=""):
        """set object status"""
        self.name = ""
        self.city = city
        self.blon = 0.0
        self.blat = 0.0
        self.phone = ""
        self.address = ""
        self.offset = -1

    def toKeyValue(self, encoding='UTF-8'):
        """generate a dict of object's properties"""
        x, y = util.coordtrans("bd09ll", "bd09mc", self.blon, self.blat)
        return {
            'id': 0,
            'point_x': int(x),
            'point_y': int(y),
            'catalog': 0,
            'name': self.name.encode(encoding, 'ignore'),
            'address': self.address.encode(encoding, 'ignore'),
            'city': self.city.encode(encoding, 'ignore'),
            'phone': self.phone.encode(encoding, 'ignore')
        }


def clean_no_brac(ustring):
    """清理字符串内容，删除其中的括号及内部内容"""
    seps = []
    left=False
    for i, char in enumerate(ustring):
        if char == u'(':
            left = True
            continue
        if char == u')':
            left = False
            continue
        if left:
            continue
        seps.append(char)
    return u''.join(seps)


def has_address_keywords(ustring):
    """是否含有地址的标识字符"""
    if (u'地址' in ustring) or \
       (u'店址' in ustring) or \
       (u'坐标' in ustring) or \
       (u'坐落' in ustring) or \
       (u'地处' in ustring) or \
       (u'位于' in ustring) or \
       (u'地点' in ustring) or \
       (u'位置' in ustring):
        return True
    return False


def has_name_keywords(ustring):
    """是否含有名称的标识字符"""
    if (u'店名' in ustring) or \
       (u'店家' in ustring) or \
       (u'名字' in ustring):
        return True
    return False


def has_phone_keywords(ustring):
    """是否含有电话的标识字符"""
    if (u'电话' in ustring) or \
       (u'座机' in ustring) or \
       (u'分机' in ustring) or \
       (u'联系方式' in ustring) or \
       (u'tel' in ustring) or \
       (u'手机' in ustring):
        return True
    return False


def logic_length(ustring):
    """英文单词长度为一， 数字长度为一的字符串长度"""
    u = uni.uniform(ustring).replace('\t', ' ').strip()
    if u.isalpha():
        return 3
    pieces = u.split(' ')
    length = 0
    insec = False
    for each in pieces:
        if each.isalpha():
            length += 1
            continue
        for ch in each:
            if uni.is_number(ch) or uni.is_alphabet(ch):
                if not insec:
                    insec = True
                    length += 1
            else:
                insec = False
                length += 1
    return length


def useful_sentence(ustring, jud):
    """是否是有用的句子, 有意义, 不包含stopwords等"""

    if  jud.name_accept(ustring) or jud.addr_accept(ustring):
        return True

    if (len(ustring) < 2 or jud.skip(ustring)) and \
       (not has_name_keywords(ustring)) and \
       (not has_address_keywords(ustring)) and \
       (not has_phone_keywords(ustring)):
        return False

    if (u'人均' in ustring) or \
       (u'原创' in ustring) or \
       (u'转载' in ustring) or \
       (ustring[-1] == u'元' and uni.is_number(ustring[-2])):
        return False

    if (u'营业' in ustring) or \
       (u'时间' in ustring) or \
       (u':15' in ustring) or \
       (u':30' in ustring) or \
       (u':45' in ustring) or \
       (u':00' in ustring):
        return False

    if (u'推荐' in ustring or u'指数' in ustring or u'评分' in ustring) and \
       (not has_name_keywords(ustring)) and \
       (not has_address_keywords(ustring)) and \
       (not has_phone_keywords(ustring)):
        return False

    if jud.refuse(ustring) and jud.refuse(clean_no_brac(ustring)):
        return False

    return True



def cleansegs(words):
    """整合分词导致的市区分离的情况(patch)"""
    usegs = []
    for each in words:
        if len(each) == 1 and (each in (u'市', u'区')) and usegs:
            usegs[-1] += each
        else:
            usegs.append(each)
    return usegs


pth = '../biz/data/'
jud = Judge.Judge(pth + 'refuse.keys',
                  pth + 'addr.accept.keys',
                  pth + 'name.accept.keys',
                  pth + 'name.suffix.keys',
                  pth + 'skip.keys')

trie = Trie.Trie(host='10.207.202.23', port=8089)

balancer = biz.balance.Balancer()
rpcpool = ThreadPool(60)

cwd = os.getcwd()
sys.path.append('.')
os.chdir('../biz/')
sofa = __import__('sofa')
segmentor = Segmentor()
os.chdir(cwd)
city_predictor = citypred.CityGeoTree('../biz/GEO_TREE/place.txt')


class ShortSentence(object):
    """短句对象, 记录句子和句子索引"""

    def __init__(self, ustring, idx):
        self._ustr = ustring
        self.idx = idx

    def str(self):
        """返回具体短句"""
        return self._ustr


def pharse(js):
    """解析句子, 得出短句"""
    global jud
    shorts = []
    for i, each in enumerate(js):
        if each['type'] != 'text' and each['type'] != 'poi':
            continue
        if has_address_keywords(each['data']) or jud.addr_accept(each['data']):
            shorts.extend([ShortSentence(each['data'].replace(u' ', ''), i)])
            continue
        tmp = uni.string2normal(each['data']) if each['type'] == 'text' else \
                [each['data']['poiName'],
                 each['data']['address'],
                 each['data'].get('phone', '')]
        shorts.extend([ShortSentence(ustr.replace(u' ', ''), i) for ustr in tmp])
    return shorts, len(js)


def predict_city(js):
    """预测城市"""
    global segmentor, city_predictor
    allsentences = []
    for each in js:
        if each['type'] == u'text':
            allsentences.append(each['data'].decode('UTF-8'))
        if each['type'] == u'poi':
            allsentences.append(each['data']['poiName'].decode('UTF-8'))
            allsentences.append(each['data']['address'].decode('UTF-8'))
    allsegs = segmentor.seg((u' '.join(allsentences)).encode('GBK', 'ignore'))
    _city = city_predictor.predict(cleansegs(allsegs))
    if _city is None:
        _city = ""
    return _city


def searching_for_address(short_sentences, ele_num):
    """搜索句子中的地址"""
    global jud
    address = []
    filterd_sentences = []
    address_appears = [0] * ele_num
    for sen in short_sentences:
        txt = sen.str()
        if not useful_sentence(txt, jud):
            continue
        if (has_address_keywords(txt) or jud.addr_accept(txt)) and \
           (not jud.refuse(txt)) and (not has_phone_keywords(txt)) and\
           logic_length(txt) > 4:
            if (u":" in txt) and (not has_address_keywords(txt)):
                address.append((txt.split(':', 1)[1].strip(), sen.idx))
            else:
                address.append((txt.replace(u'地址', '').strip(), sen.idx))
            address_appears[sen.idx] = 1
            continue
        filterd_sentences.append(sen)
    return filterd_sentences, address, address_appears


def address_cluster_by_dense(appears, addresses):
    """聚合地址段, 区分单地址与连续多地址段"""
    threshold = 0.399
    agglen = 5
    ranges = []
    start = -1
    end = -1
    for i in range(len(appears)):
        if sum(appears[i:i + agglen]) * 1.0 / agglen > threshold:
            if start < 0 and end < 0:
                start = i
            end = i + agglen if i + agglen < len(appears) else len(appears) - 1
        else:
            if end > 0:
                ranges.append((start, end))
                start, end = -1, -1
    if end > 0:
        ranges.append((start, end))
        start, end = -1, -1
    address_cluster = []
    address_single = []
    cluster = []
    last_end = 0
    name_begin = 0
    for (a, ai) in addresses:
        if ranges:
            found = False
            for pair in ranges:
                if pair[0] <= ai <= pair[1]:
                    cluster.append((a, ai, last_end))
                    if last_end - pair[1] > agglen:
                        last_end = pair[1]
                    found = True
                    break
                else:
                    if cluster:
                        address_cluster.append(cluster)
                        cluster = []
            if cluster and found:
                address_cluster.append(cluster)
                cluster = []
            if not found:
                address_single.append((a, ai, name_begin))
                name_begin = ai
                last_end = pair[1]
        else:
            address_single.append((a, ai, name_begin))
            name_begin = ai
    return address_single, address_cluster


def call_rpc(pair):
    """call rpc check-poi-single"""
    poi, _rpc = pair
    payload = poi.toKeyValue(encoding='GBK')
    response = json.loads(_rpc.check_poi_single(**payload), encoding='GBK')
    return poi, response


def Article(aid, title, content, only_name=False, debug=False):
    """POI抽取"""
    global jud, trie, rpcpool
    respon = ArtResponse(aid, mkpoi, debug=debug)

    js = json.loads(content, encoding='UTF-8')
    _city = predict_city(js)
    short_sentences, ele_num = pharse(js)

    _sentences, respon.all_addresses, appears = searching_for_address(short_sentences, ele_num)
    if not respon.all_addresses:
        return respon.toKeyValue()

    addsingle, addcluster = address_cluster_by_dense(appears, respon.all_addresses)
    respon.names = trie.search(_sentences, _city)


    unique_pois = set()
    pois = []
    if addsingle and respon.names:
        for (n, ni) in respon.names:
            for (a, ai, begin) in addsingle:
                fingerprint = u'%s%s' % (n, a)
                if ai >= ni >= begin and (fingerprint not in unique_pois):
                    poi = POI()
                    poi.city, poi.name, poi.address, poi.offset = _city, n, a, ai
                    pois.append(poi)
    if addcluster and respon.names:
        for (n, ni) in respon.names:
            for cluster in addcluster:
                for (a, ai, begin) in cluster:
                    fingerprint = u'%s%s' % (n, a)
                    if ai >= ni >= begin and (fingerprint not in unique_pois):
                        poi = POI()
                        poi.city, poi.name, poi.address, poi.offset = _city, n, a, ai
                        pois.append(poi)

    if not pois:
        return respon.toKeyValue()

    panchong_results = rpcpool.map(call_rpc, [(poi, balancer.fetch_one()) for poi in pois])

    for poi, presult in panchong_results:
        respon.debuginfo.append(poi.toKeyValue('UTF-8'))
        ps = []
        if presult['msg'] == u'SUCCESS' and presult['list'][0]['is_duplicate'] == u'duplicate':
            myid = presult['list'][0]['compare_ret'][0]['volunteer_id']
            if myid not in respon.pids:
                respon.pids.append(presult['list'][0]['compare_ret'][0]['volunteer_id'])
                ps.append({
                    'type': 'poi',
                    'data': mkpoi.mkpoi(myid)
                })
        if ps:
            respon.mypois[poi.offset] = ps

    return respon.toKeyValue()

if __name__ == '__main__':
    #print segmentor.seg(u'中文分词'.encode('GBK'))

    print searching_for_address([ShortSentence(u'20分钟pm2', 0)], 1)
