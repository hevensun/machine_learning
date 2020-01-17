#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/12/3 9:40 AM
# @Author  : Slade
# @File    : main.py

from model import Neologism
import pandas as pd
import numpy as np

df = pd.read_csv("/Users/slade/Desktop/cargo_name01.csv")
text = '，'.join(np.column_stack(df.values).tolist()[0])

text_base = Neologism(st=text, prev_cut=True, macth_posseg=[["a"], ["n"]])
print(text_base.filter(frequency=0.001, freedom=0.5))

direct_search = Neologism(st=text, prev_cut=False)
print(direct_search.filter(frequency=0.0001, polymerization=15, freedom=0.5))
