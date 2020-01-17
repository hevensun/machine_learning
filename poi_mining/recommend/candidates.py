# -*- encoding: utf-8 -*-
"""
Main Logic Level, essential part of this level is to do recommendation base on diff scence

核心业务层，主要功能为切合业务需求，做相关相识度门店推荐，实际内容推荐层，如设计初衷所描述，业务衍生内容建议以衍生类进行处理封装，可能存在的问题（当业务内容过于庞大，类类型繁多，文件代码过大，将导致管理繁琐）。解决方案，建议该层以文件夹作为层级管理，以基础类为主文件，各业务推荐独自管理各自类文件。
"""
import sys
import requests
import json
import operator
import time

BRAND_URL = "http://10.194.219.37:8003/brand_parse"
DISH_URL = "http://10.194.219.37:8003/dish_parse"

class BaseCandidateModel(object):
    """
    Base Candidate Model
    """
    
    def __init__(self):
        """
        """
        self.candidates = {"base": {}}
        self.info = {"__candidate_level__": ""}

    @classmethod
    def search(cls, article):
        """
        virtual search function
        """
        pass


class BrandCandidateModel(BaseCandidateModel):
    """
    Brand Shop Candidate Search
    """

    def __init__(self):
        """
        """
        super(BaseCandidateModel, self).__init__()

    @classmethod
    def search(cls, article):
        """
        """
        _data = []
        article = json.loads(article)
        for ele in article:
            if ele["type"] == "text": _data.append(ele["data"])
        data = {"sentences": json.dumps(_data), "city": ""}

        r = requests.post(BRAND_URL, data)

        _res = dict()
        for key, value in r.json()['data'].iteritems():
            if len(value) < 1: continue
            _res[key] = value
            
        return _res


class DishCandidateModel(BaseCandidateModel):
    """
    Dish Shop Candidate Search
    """

    def __init__(self):
        """
        """
        super(BaseCandidateModel, self).__init__()

    @classmethod
    def search(cls, article):
        """
        """
        THRESHOLD = 3
        _data = []
        article = json.loads(article)
        for ele in article:
            if ele["type"] == "text": _data.append(ele["data"])
        data = {"sentences": json.dumps(_data), "city": ""}

        r = requests.post(DISH_URL, data)

        # data format of _data
        # {"dish_name01": [{"shop_id":, "city": }, ]}
        _data = r.json()['data']
        _res = dict()
        # count number of dish each shop have been mentioned
        for key, value in _data.iteritems():
            for ele in value: 
                local_key = ele["shop_id"] + ":" + ele["city"]
                if local_key not in _res: _res[local_key] = 0
                _res[local_key] += 1
        
        # count how many dish be recommend in each shop, get top 3
        target = dict()
        _res = sorted(_res.items(), key=operator.itemgetter(1), reverse=True)
        _count = dict()
        for key, value in _res:
            bid, city = key.split(":")
            if city not in _count: _count[city] = 0
            if _count[city] >= 3: continue
            target[key] = 0
            _count[city] += 1

        res = dict()
        for key, value in _data.iteritems():
            if key not in res: res[key] = []
            for ele in value:
                local_key = ele["shop_id"] + ":" + ele["city"]
                if local_key in target: res[key].append(ele)
        return res


if __name__ == "__main__":
    reload(sys)
    sys.setdefaultencoding("utf-8")
