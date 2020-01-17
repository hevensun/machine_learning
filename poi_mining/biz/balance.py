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
简单连接池
"""

import rpc
import json
import random
import commands
from Queue import Queue
from threading import Thread


class Balancer(object):
    """判重服务负载处理"""

    def __init__(self):
        self.hostnames = []
        self.rpcs = []
        self.bns = 'strategy-service-pm-panchong.nuomi.sh01'
        self.nslookup()
        self.connect()

    def nslookup(self):
        """nslookup for baidu bns"""
        if len(self.hostnames) == 0:
            st, out = commands.getstatusoutput('get_instance_by_service %s' % self.bns)
            assert st == 0, "Failure:'get_instance_by_service %s', errno=%d" % (self.bns, st)
            self.hostnames = out.split('\n')
        assert self.hostnames, 'No hosts found for bns: "%s"' % self.bns

    def connect(self):
        """init connection"""
        if len(self.rpcs) == 0 and len(self.hostnames) > 0:
            for host in self.hostnames:
                self.rpcs.append(rpc.RPC(host=host, port=8000))
        assert self.rpcs, "init poi-compare failure!"

    def fetch_one(self):
        """random fetch"""
        return random.choice(self.rpcs)


