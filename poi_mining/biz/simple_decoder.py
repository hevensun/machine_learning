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
docstring for module
"""


import json

def _byteify_utf8(data, ignore_dicts=False):
    """xxx """
    # if this is a unicode string, return its string representation
    if isinstance(data, unicode):
        return data.encode("utf-8")
    # if this is a list of values, return list of byteified values
    if isinstance(data, list):
        return [_byteify_utf8(item, ignore_dicts=True) for item in data]
    # if this is a dictionary, return dictionary of byteified keys and values
    # but only if we haven't already byteified it
    if isinstance(data, dict) and not ignore_dicts:
        return {
            _byteify_utf8(key, ignore_dicts=True): _byteify_utf8(value, ignore_dicts=True)
            for key, value in data.iteritems()
        }
    # if it's anything else, return it in its original form
    return data


def _byteify_gbk(data, ignore_dicts=False):
    """xxx """
    # if this is a unicode string, return its string representation
    if isinstance(data, unicode):
        return data.encode("gbk")
    # if this is a list of values, return list of byteified values
    if isinstance(data, list):
        return [_byteify_gbk(item, ignore_dicts=True) for item in data]
    # if this is a dictionary, return dictionary of byteified keys and values
    # but only if we haven't already byteified it
    if isinstance(data, dict) and not ignore_dicts:
        return {
            _byteify_gbk(key, ignore_dicts=True): _byteify_gbk(value, ignore_dicts=True)
            for key, value in data.iteritems()
        }
    # if it's anything else, return it in its original form
    return data


if __name__ == "__main__":
    s  = '{"field1":null, "field2": "data!", "name":"你"}'
    #print json.loads(s,object_hook = _byteify)


