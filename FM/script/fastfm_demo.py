# fast_fm used in classification cases
'''
    __author__ = 'sladesal'
    __time__ = '20171124'
    __blog__ = 'www.shataowei.com'
    rank：潜在因子的个数
    n_iter：数据循环的次数
    l2_reg_w：w矩阵的限制大小
    l2_reg_V：v矩阵的限制大小
    init_stdev：所有数据的方差限制
    l2_reg：w0值
    step_size：梯度下降的学习速率
'''

import pandas as pd
import numpy as np
from fastFM import sgd
from sklearn import preprocessing
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import mean_squared_error, r2_score
import sys

# 加载数据
def load_data(path):
    feature = []
    tag = []
    f = open(path)
    N = 0
    for i in f.readlines():
        if N > 0:
            info = i.strip().split('\t')
            indiv_line = []
            for j in range(2, len(info)):
                indiv_line.append(np.float(info[j]))
            feature.append(indiv_line)
            tag.append(np.float(info[1]))
        N = N + 1
    return np.mat(feature), np.array(tag)

# 处理因变量
def change_tag_format(tag):
    tag[tag == 0] = -1
    return tag

#onehotencoding
def ohe(feature):
    ohe = OneHotEncoder()
    ohe.fit(feature)
    return ohe.transform(feature)

# 数据分段处理
def slice_data(feature):
    for i in range(feature.shape[1]):
        if len(pd.DataFrame(feature[:, i]).drop_duplicates()) > 5:
            t1 = np.percentile(np.array(feature[:, i].ravel())[0], 20)
            t2 = np.percentile(np.array(feature[:, i].ravel())[0], 40)
            t3 = np.percentile(np.array(feature[:, i].ravel())[0], 60)
            t4 = np.percentile(np.array(feature[:, i].ravel())[0], 80)
            for j in range(feature[:, i].shape[0]):
                if feature[j, i] <= t1:
                    feature[j, i] = '0'
                elif feature[j, i] > t1 and feature[j, i] <= t2:
                    feature[j, i] = '1'
                elif feature[j, i] > t2 and feature[j, i] <= t3:
                    feature[j, i] = '2'
                elif feature[j, i] > t3 and feature[j, i] <= t4:
                    feature[j, i] = '3'
                else:
                    feature[j, i] = '4'
        print('ready over the no. %s times of %s times' %(i,feature.shape[1]))
    return feature

#rate score
def precision_score(y_true, y_pred):
    return ((y_true==1)*(y_pred==1)).sum()/(y_pred==1).sum()

def recall_score(y_true, y_pred):
    return ((y_true==1)*(y_pred==1)).sum()/(y_true==1).sum()

def f1_score(y_true, y_pred):
    num = 2* precision_score(y_true, y_pred)*recall_score(y_true, y_pred)
    deno = (precision_score(y_true, y_pred)+recall_score(y_true, y_pred))
    return num/deno

if __name__ == '__main__':
    # 定义处理数据
    path = sys.argv[1]
    feature, tag = load_data(path)
    tag = change_tag_format(tag)
    feature = slice_data(feature)
    feature = ohe(feature)
    # 定义分类器
    sf = sgd.FMClassification(n_iter=500, l2_reg_w=0.1, l2_reg_V=0.1, rank=20)
    sf.fit(feature, tag)
    y_ = sf.predict(feature)
    y_p = sf.predict_proba(feature)
    print(y_)
    print(y_p)
    print('all over the running process')
