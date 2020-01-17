# -*- encoding: utf-8 -*-
"""
排序的主要目的，在于辅助业务，提升POI的点击转化率，因此我们在此为其单拎为一层。基础排序内容为，提升用户体验，推荐高质量门店，但该内容可能会因业务而有所侧重。
"""

import sys
import json

class BaseRankModel(object):
    """
    Base Rank Model 
    """

    def __init__(self):
        self.info = {"__rank_level__": ""}
        self.res = {"base": []} 

    def random(self):
        """
        random rank shop
        """
        pass

    def top_n(self, dic, n):
        """
        get top n shops
        """
        pass

    @classmethod
    def run(cls, candidates):
        """
        main function
        """
        n = 10
        if type(candidates) is not dict: return {}
        if "base" not in candidates: return {}
        res = dict()
        for key, value in candidates["base"].iteritems():
            if key not in res: res[key] = dict()
            for sub_key, sub_value in value.iteritems():
                if len(sub_value) == 0: continue
                if len(sub_value) < n: res[key][sub_key] = sub_value
                if len(sub_value) >= n: res[key][sub_key] = sub_value[0:n]
        return res


if __name__ == "__main__":
    reload(sys)
    sys.setdefaultencoding("utf-8")
