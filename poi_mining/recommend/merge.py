# -*- encoding: utf-8 -*-
"""
Merge Level, main purpose is to combine and filter recommend result come from recommend-logic level

候选集融合（文件: merge.py）, 如名字所描述，该层为候选集结果融合和过滤，如基于POI门店质量进行过滤等。
"""

import sys
import traceback
from collections import Counter

class BaseMergeModel(object):
    """
    Base Merge Model
    """

    def __init__(self):
        """
        """
        self.res = {"base": []}
        self.info = {"__merge_level__": ""}
        pass

    @classmethod
    def run(cls, candidates):
        """
        main function
        """
        if type(candidates) is not dict: return {}
        return candidates


class GlobalMergeModel(BaseMergeModel):
    """
    Merge model that merge result of precise match and recommend
    """

    def __init__(self):
        """
        Empty
        """
        super(BaseCandidateModel, self).__init__()

    @classmethod
    def run(cls, content, recommend, city_id, city_name, N=10):
        """
        Main Merge Function
        """
        _res = [] # if exist poi belong to given city_id
        _back = []
        # if "poiNum" in content and content["poiNum"] > 0:
        #   _res = [str(ele) for ele in content["poiList"][0:N]]
        # if len(_res) == N: return _res
        
        half = (N - len(_res)) // 2
        try:
            key, value = "brand", recommend["base"]["brand"]
            _data = sorted(value, key=len, reverse=True)
            for ele in _data:
                for ent in value[ele]:
                    if len(_res) == half: break
                    if city_id is "" or city_id is None:
                        _res.append(ent["shop_id"])
                    elif city_id == ent["city"]:
                        _res.append(ent["shop_id"]) # filter by city_id

                    _back.append(ent["shop_id"])
                if len(_res) == half: break
            
            _back = _back[0:half]

            half = (N - len(_res))
            _half = (N - len(_back))
            
            key, value = "dish", recommend["base"]["dish"]
            count = Counter()
            _c = Counter()
            for ele, ele_value in value.iteritems():
                for ent in ele_value:
                    if city_id is "" or city_id is None:
                        count[ent["shop_id"]] += 1
                    elif city_id == ent["shop_id"]:
                        count[ent["shop_id"]] += 1

                    _c[ent["shop_id"]] += 1
            most = count.most_common(half)
            _most = _c.most_common(_half)
            for ele in most:
                _res.append(ele[0])
            
            for ele in _most:
                _back.append(ele[0])

        except Exception as e:
            print traceback.print_exc()
        
        if len(_res) > 0:
            return _res
        else:
            return _back



if __name__ == "__main__":
    reload(sys)
    sys.setdefaultencoding("utf-8")
