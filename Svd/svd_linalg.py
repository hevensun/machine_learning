# -*- coding:utf8 -*-
from numpy import *
from numpy import linalg as la
import pandas as pd

datamat = mat([[0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 5],
               [0, 0, 0, 3, 0, 4, 0, 0, 0, 0, 3],
               [0, 0, 0, 0, 4, 0, 0, 1, 0, 4, 0],
               [3, 3, 4, 0, 0, 0, 0, 2, 2, 0, 0],
               [5, 4, 5, 0, 0, 0, 0, 5, 5, 0, 0],
               [0, 0, 0, 0, 5, 0, 1, 0, 0, 5, 0],
               [4, 3, 4, 0, 0, 0, 0, 5, 5, 0, 1],
               [0, 0, 0, 4, 0, 4, 0, 0, 0, 0, 4],
               [0, 0, 0, 2, 0, 2, 5, 0, 0, 1, 2],
               [0, 0, 0, 0, 5, 0, 0, 0, 0, 4, 0],
               [1, 0, 0, 0, 0, 0, 0, 1, 2, 0, 0]]

# 欧拉距离相似度，评分可用，程度不建议


def oulasim(A, B):
    distince = la.norm(A - B)  # 第二范式：平方的和后求根号
    similarity = 1 / (1 + distince)
    return similarity


# 余弦相似度，评分、1/0、程度都可以用
def cossim(A, B):
    ABDOT = dot(A, B)
    ABlen = la.norm(A) * la.norm(B)
    if ABlen == 0:
        similarity = '异常'
    else:
        similarity = ABDOT / float(ABlen)
    return similarity


# 皮尔逊相关系数
def pearsonsim(A, B):
    A = A - mean(A)
    B = B - mean(B)
    ABDOT = dot(A, B)
    ABlen = la.norm(A) * la.norm(B)
    if ABlen == 0:
        similarity = '异常'
    else:
        similarity = ABDOT / float(ABlen)
    return similarity


# 协同推荐，商品相似度打分
def recommender(datamat, item_set, method):
    col = shape(datamat)[1]  # 物品数量
    item = datamat[:, item_set]
    similarity_matrix = zeros([col, 1])
    for i in range(col):
        index = nonzero(logical_and(item > 0, datamat[:, i] > 0))[0]
        if sum(index) > 0:
            similarity = method(datamat[index, item_set].T, datamat[index, i])
        else:
            similarity = '-1'
        similarity_matrix[i] = similarity
    return similarity_matrix


# 相似度矩阵
def similarity(datamat, method):
    item_sum = shape(datamat)[1]
    similarity = pd.DataFrame([])
    for i in range(item_sum):
        res = recommender(datamat, i, method)
        similarity = pd.concat([similarity, pd.DataFrame(res)], axis=1)
    return similarity


# svd
n = shape(datamat)[1]  # 商品数目
U, sigma, VT = la.svd(datamat)

# 规约最小维数
sigma2 = sigma ** 2
k = len(sigma2)
n_sum2 = sum(sigma2)

nsum = 0
max_sigma_index = 0
for i in sigma:
    nsum = nsum + i ** 2
    max_sigma_index = max_sigma_index + 1
    if nsum >= n_sum2 * 0.9:
        break

# item new matrix
item = datamat.T * U[:, 0:max_sigma_index] * sigma[0:max_sigma_index]
