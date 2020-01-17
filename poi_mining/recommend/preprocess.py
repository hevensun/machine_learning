# -*- encoding: utf-8 -*-
"""
Preprocess article, include format cleaning, quality esimation and property checking, etc.
处理文章内容，对文章进行初步判定（如文章质量是否合格，文章是否符合品牌推荐，文章是否符合推荐菜门店推荐标准等），该层封装初步的文章『整体』质量的评估，并对文章进行候选模块的分发。
"""
import sys
from candidates import BaseCandidateModel
from candidates import BrandCandidateModel
from candidates import DishCandidateModel
from merge import BaseMergeModel
from rank import BaseRankModel

class BaseProcessModel(object):
    """
    Base Process Model
    """
    pass

    def __init__(self, article, recommend_type=None):
        """
        Parameter
            - recommend_type: brand, dish, business_type, ...
        """
        self.info = {"__preprocess_level__": ""}
        self.article = article
        self.recommend_type = recommend_type

    def quality_checking(self):
        """
        Quality Checking
        """
        # check article length
        if len(self.article) < 5: return False
        return True

    def run(self):
        """
        Run
        """
        if not self.quality_checking():
            self.info["__preprocess_level__"] = "Article Quality Couldn't Pass Test"
            return
        
        if len(self.recommend_type) == 0:
            self.info["__preprocess_level__"] = "Not Recommend_Type Have Been Passed"
            return

        res = BaseCandidateModel()
        for ele in self.recommend_type:
            if ele == "brand":
                res.candidates["brand"] = BrandCandidateModel.search(self.article)
            if ele == "dish":
                res.candidates["dish"] = DishCandidateModel.search(self.article)

        _local_merge = BaseMergeModel()
        _local_merge.res["base"] = BaseMergeModel.run(res.candidates)

        _local_rank = BaseRankModel()
        _local_rank.res["base"] = BaseRankModel.run(_local_merge.res)
        return _local_rank.res


if __name__ == "__main__":
    reload(sys)
    sys.setdefaultencoding("utf-8")

