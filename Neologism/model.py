#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/12/3 9:40 AM
# @Author  : Slade
# @File    : model.py

import jieba.posseg as jp
import re
from PyTls import textt
import math
import numpy as np


class Neologism(object):
    def __init__(self, st, prev_cut=False, macth_posseg=None, max_word_length=4):
        # 参数指定
        self.prev_cut = prev_cut
        self._all_sub_sentence_length = 0
        self.max_word_length = max_word_length
        self.word_map = {}

        # 是否需要预先切词做已知词拓展
        if self.prev_cut:
            self.cut = jp.lcut
            if len(macth_posseg) == 1:
                self.start_posseg = macth_posseg
                self.end_posseg = macth_posseg
            elif len(macth_posseg) == 2:
                self.start_posseg = macth_posseg[0]
                self.end_posseg = macth_posseg[1]
            else:
                raise TypeError()

        # 预处理
        self.read_string(st=st)
        self.handle()

    def read_string(self, st, split_seq='[，。！？：]'):
        """
        讲字符按照split_seq格式来分割
        :param st: 字符串
        :param split_seq: 字符分割
        :return: None
        """
        ls = re.split(split_seq, st)
        self.read_ls(ls=ls)

    def clean(self, data):
        '''
        去除非中文
        :param data:
        :return:
        '''
        usentence = [uchar for uchar in data if '\u4e00' <= uchar <= '\u9fa5']
        return ''.join(usentence), len(usentence)

    def read_ls(self, ls):
        '''
        处理非中文子段落，并把长度大于2的进行分词处理
        :param ls:
        :return:
        '''
        for sub in ls:
            clean_data, lens = self.clean(data=sub)
            if lens > 2:
                self.split(clean_data, lens)

    def split(self, words, lens):
        '''
        拆分字符，最大匹配num个字符，并也字典的形式返回，
        :param words:
        :param lens:
        :return: 新词发现：[出现次数,出现频率,凝固程度,自由程度,关键字的左邻,关键字的右邻]；
                已知词扩展：[出现次数,出现频率,凝固程度,自由程度,关键字的左邻,关键字的右邻，当前词词性]
        '''
        if self.prev_cut:
            words = self.cut(words)
            lens = len(words)
            self._all_sub_sentence_length += lens
            for idx in range(lens):
                if self.word_map.get(words[idx].word):
                    self.word_map[words[idx].word][0] += 1

                    # 异常处理
                    if idx != 0 and words[idx - 1].word not in self.word_map[words[idx].word][4]:
                        self.word_map[words[idx].word][4].append(words[idx - 1].word)
                    if idx != lens - 1 and words[idx + 1].word not in self.word_map[words[idx].word][5]:
                        self.word_map[words[idx].word][5].append(words[idx + 1].word)
                else:
                    self.word_map[words[idx].word] = [1, 0.0, 1, 0, [] if idx == 0 else [words[idx - 1].word],
                                                      [] if idx == lens - 1 else [words[idx + 1].word], words[idx].flag]
        else:
            self._all_sub_sentence_length += lens
            for i in range(0, lens):
                for j in range(1, self.max_word_length + 1):
                    if i + j <= lens:
                        key = words[i:i + j]
                        if self.word_map.get(key):
                            self.word_map[key][0] += 1
                            if i != 0 and words[i - 1] not in self.word_map[key][4]:
                                self.word_map[key][4].append(words[i - 1])
                            if i + j != lens and words[i + j] not in self.word_map[key][5]:
                                self.word_map[key][5].append(words[i + j])
                        else:
                            self.word_map[key] = [1, 0.0, 1, 0, [] if i == 0 else [words[i - 1]],
                                                  [] if i + j == lens else
                                                  [words[i + j]]]

    def handle(self):
        '''
        核心计算逻辑，包括左右出现词的信息熵，词内部的聚合度，词频更新，扩展词词性过滤等
        :return:
        '''
        # 更新出现频率
        for key in self.word_map.keys():
            self.word_map[key][1] = self.word_map[key][0] / self._all_sub_sentence_length

        if self.prev_cut:
            for key in self.word_map.keys():
                word_list = self.word_map[key]
                if len(key) == 1:
                    continue
                end_all = front_all = 0.0

                front_list = []
                for front in word_list[4]:
                    if self.word_map.get(front) and self.word_map.get(front)[-1] in self.start_posseg:
                        entory = -math.log(self.word_map[front][1]) * self.word_map[front][1]
                        front_all += entory  # 左邻字的信息熵
                        front_list.append(self.word_map[front][1])
                    else:
                        front_list.append(0)

                end_list = []
                for end in word_list[5]:
                    if self.word_map.get(end) and self.word_map.get(end)[-1] in self.end_posseg:
                        entory = -math.log(self.word_map[end][1]) * self.word_map[end][1]
                        end_all += entory  # 右邻字的信息熵
                        end_list.append(self.word_map[end][1])
                    else:
                        end_list.append(0)
                # 左邻字集合的信息熵和右邻字集合的信息熵的相比较
                # 最大信息熵仍小于阈值则说明该词不是一个完整的词的概率更高，需要进行左右扩充
                word_list[3] = front_all if front_all > end_all else end_all
                # 选取熵小侧作为待合并侧
                word_list[2] = word_list[4][
                                   np.argmax(front_list)] + key if front_all < end_all and sum(front_list) else key + \
                                                                                                                word_list[
                                                                                                                    5][
                                                                                                                    np.argmax(
                                                                                                                        end_list)] if sum(
                    end_list) else key
        else:
            for key in self.word_map.keys():
                word_list = self.word_map[key]
                if len(key) == 1:
                    continue
                end_all = front_all = 0.0
                left = word_list[1] / (self.word_map[key[0]][1] * self.word_map[key[1:]][1])  # 左邻凝合程度
                right = word_list[1] / (self.word_map[key[-1]][1] * self.word_map[key[:-1]][1])  # 右邻凝合程度

                for front in word_list[4]:
                    if self.word_map.get(front):
                        front_all -= math.log(self.word_map[front][1]) * self.word_map[front][1]  # 左邻字的信息熵

                for end in word_list[5]:
                    if self.word_map.get(end):
                        end_all -= math.log(self.word_map[end][1]) * self.word_map[end][1]  # 右邻字的信息熵

                # 找出左右邻凝合程度中更小作为内部凝聚度
                # 最小凝聚度仍大于阈值则说明这些字看作一个整体的词的概率更高
                word_list[2] = left if left < right else right

                # 左邻字集合的信息熵和右邻字集合的信息熵的相比较
                # 谁的信息熵越少说明该集合提供的信息越大
                # 最小信息熵仍大于阈值则说明该词看作单独的词的概率更高
                word_list[3] = front_all if front_all < end_all else end_all

    def filter(self, frequency, polymerization=None, freedom=None, strict=True, target_posseg="n"):
        """
        过滤一些不重要的数据
        :param frequency: 过滤的频率
        :param polymerization:过滤凝聚度,只有新词发现有，已知词扩展不需要指定
        :param freedom:过滤自由度
        :param strict: 是否是并且还是或者,默认是或者，满足一个就过滤
        :param target_posseg:需要发现的新词词性限制
        :return:新词发现：[出现次数,出现频率,凝聚程度,自由程度]；已知词扩展：[出现次数,出现频率,扩充词,自由程度]
        """
        key_words = dict()
        if self.prev_cut:
            for key in self.word_map.keys():
                one_word = self.word_map[key]
                if len(key) <= 1 or one_word[-1] != target_posseg:
                    continue
                if strict:
                    if one_word[1] > frequency and one_word[3] < freedom:
                        key_words[key] = [one_word[0], one_word[1], one_word[2], one_word[3]]
                else:
                    if one_word[1] > frequency or one_word[3] < freedom:
                        key_words[key] = [one_word[0], one_word[1], one_word[2], one_word[3]]
        else:
            for key in self.word_map.keys():
                one_word = self.word_map[key]
                if len(key) <= 1:
                    continue
                if strict:
                    if one_word[1] > frequency and one_word[2] > polymerization and one_word[3] > freedom:
                        key_words[key] = [one_word[0], one_word[1], one_word[2], one_word[3]]
                else:
                    if one_word[1] > frequency or one_word[2] > polymerization or one_word[3] > freedom:
                        key_words[key] = [one_word[0], one_word[1], one_word[2], one_word[3]]
        return key_words
