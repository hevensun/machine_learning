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
API 接口文件
"""

import sys
import traceback
sys.path.append('../')
from biz import poi_extraction as pex
from recommend import preprocess as pro
from recommend import merge as mg
import json

class Processer(object):
    """ 请求数据类对象 """

    def __init__(self, logger):
        self.logger = logger

    def run(self, request, response):
        """ 判断文章中是否有POI """
        try:
            response.errno = "0"          # 错误号 0-成功 非0失败，可自定义列出详细错误号
            response.errmsg = "success" # 错误内容
            response.content = pex.Article(request.aid, "", request.content, debug=request.debug)
            # if we get precise match then we return
            if response.content["poiNum"] > 0: 
                response.display = response.content["poiList"][0:10] 
                return 
            response.recommend = pro.BaseProcessModel(request.content, ["brand", "dish"]).run() 
            response.display = mg.GlobalMergeModel.run(response.content, 
                                                       response.recommend, 
                                                       request.city_id, 
                                                       request.city_name)
        except Exception as e:
            traceback.print_exc()


if __name__ == "__main__":
    pass
