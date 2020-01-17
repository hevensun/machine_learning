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

import urllib2
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import datetime
from input import RequestData
from output import ResponseData
from processer import Processer
from tornado.options import define
from tornado.options import options
from log import EasyLog

define("port", default=8881, help="run on the given port", type=int)

class MainHandler(tornado.web.RequestHandler):
    """
    服务处理类
    """

    logger = EasyLog()
    logger.init_log("../logs/poi")

    def initialize(self):
        """
        初始化
        """
        # 初始化日志
        # 数据初始化
        self.request_data = RequestData()
        self.response_data = ResponseData()
        self.processer = Processer(self.logger)

    def get(self):
        """
        处理get请求
        """
        return self.run()

    def post(self):
        """
        处理post请求
        """
        return self.run()

    def run(self):
        """
        处理post请求
        """
        # 解析传入参数
        self.request_data.reset()
        self.request_data.aid = self.get_argument('globalId')
        self.request_data.content = urllib2.unquote(str(self.get_argument('content')))
        self.request_data.city_id = self.get_argument('city_id', default="")
        self.request_data.city_name = self.get_argument('city_name', default="")
        self.request_data.debug = False if self.get_argument('debug', "false") == 'false' else True
        #self.log_req()
        # 创造传出参数
        self.response_data.reset()
        start_time = datetime.datetime.now()
        self.processer.run(self.request_data, self.response_data)
        end_time = datetime.datetime.now()
        run_time = "运行时间:" + str(end_time - start_time) + "微秒"
        MainHandler.logger.info(run_time)
        #self.log_res()
        self.write(self.response_data.package())

    def log_req(self):
        """
        打印请求日志信息
        """
        ip = self.request.remote_ip
        path = self.request.uri
        #body = self.request.body
        body = self.request_data.tostr()
        request = "Request[" + ip + "]" + "[" + path + "]" + "[" + body + "]"
        MainHandler.logger.info(request)

    def log_res(self):
        """
        打印响应日志信息
        """
        ip = self.request.remote_ip
        path = self.request.uri
        body = self.response_data.tostr()
        response = "Response[" + ip + "]" + "[" + path + "]" + "[" + body + "]"
        MainHandler.logger.info(response)


if __name__ == "__main__":
    tornado.options.parse_command_line()
    Handlers=[(r"/feed/poiRecognize", MainHandler),]
    application = tornado.web.Application(Handlers)
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
