#coding:utf-8
################################################################################
#
### Copyright (c) 2015 Baidu.com, Inc. All Rights Reserved
#
##################################################################################
"""
This module provide configure file management service in i18n environment.

Authors: wangdia01(wangdian01@baidu.com)
Date:    2015/07/14
"""
import sys
import json
reload(sys)
sys.setdefaultencoding('utf-8')

class ResponseData(object):
    """
    请求数据类对象
    """
    def __init__(self):
        """
        初始化
        """
        self.errno = None
        self.errmsg = None
        self.content = None
        self.recommend = None
        self.display = None

    def reset(self):
        """reset object status"""
        self.errno = None
        self.errmsg = None
        self.content = None

    def package(self):
        """
        将传入参数解析出来
        """
        str_res = {}
        str_res["errno"] = self.errno
        str_res["errmsg"] = self.errmsg
        str_res["data"] = self.content
        str_res["recommend"] = self.recommend
        str_res["display"] = self.display
        return str_res

    def tostr(self):
        """
        将传入参数解析出来
        """
        json_input = self.package()
        return json.dumps(json_input)

if __name__ == "__main__":
    obj = ResponseData()
    obj.errno = 0
    obj.errmsg = "success"
    obj.content = "test"
    print obj.tostr()
