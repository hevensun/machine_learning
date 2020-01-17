#coding:UTF-8
'''
    __time__ = '20171201'
    __author__ = 'sladesal'
    __blog__ = 'www.shataowei.com'
    alpha：学习速率
    iter：数据循环的次数
    dataMatrix：feature矩阵
    classLabels：因变量列表
'''

#division代表精确到小数
from __future__ import division
from math import exp
from numpy import *
from random import normalvariate#正态分布
from datetime import datetime
from sklearn import  preprocessing
import sys

def min_max(data):
    min_max_scaler = preprocessing.MinMaxScaler()
    return min_max_scaler.fit_transform(data)

def loadDataSet(data):
    #我就是闲的蛋疼，明明pd.read_table()可以直接度，非要搞这样的，显得代码很长，小数据下完全可以直接读嘛，唉～
    dataMat = []
    labelMat = []
    fr = open(data)
    N = 0
    for line in fr.readlines():
        #N=1时干掉列表名
        if N > 0:
            currLine = line.strip().split()
            lineArr = []
            featureNum = len(currLine)
            for i in range(2,featureNum):
                lineArr.append(float(currLine[i]))
            dataMat.append(lineArr)
            labelMat.append(float(currLine[1]) * 2 - 1)
        N = N + 1
    return mat(min_max(dataMat)), labelMat

def sigmoid(inx):
    #return 1.0/(1+exp(min(max(-inx,-10),10)))
    return 1.0 / (1 + exp(-inx))

#得到对应的特征weight的矩阵
def stocGradAscent(dataMatrix, classLabels, k, iter):
    #dataMatrix用的是mat, classLabels是列表
    m, n = shape(dataMatrix)
    #alpha是学习速率
    alpha = 0.01
    #初始化参数
    w = zeros((n, 1))#其中n是特征的个数
    w_0 = 0.
    v = normalvariate(0, 0.2) * ones((n, k))
    for it in range(iter):
        # 对每一个样本，优化
        for x in range(m):
            #这边注意一个数学知识：对应点积的地方通常会有sum，对应位置积的地方通常都没有，详细参见矩阵运算规则，本处计算逻辑在：http://blog.csdn.net/google19890102/article/details/45532745
            #xi·vi,xi与vi的矩阵点积
            inter_1 = dataMatrix[x] * v
            #xi与xi的对应位置乘积   与   xi^2与vi^2对应位置的乘积    的点积
            inter_2 = multiply(dataMatrix[x], dataMatrix[x]) * multiply(v, v)#multiply对应元素相乘
            #完成交叉项,xi*vi*xi*vi - xi^2*vi^2
            interaction = sum(multiply(inter_1, inter_1) - inter_2) / 2.
            # 计算预测的输出
            p = w_0 + dataMatrix[x] * w + interaction
            #计算sigmoid(y*pred_y)-1准确的说不是loss，原作者这边理解的有问题，只是作为更新w的中间参数，这边算出来的是越大越好，而下面却用了梯度下降而不是梯度上升的算法在
            loss = sigmoid(classLabels[x] * p[0, 0]) - 1
            if loss >= -1:
                loss_res = '正方向 '
            else:
                loss_res = '反方向'
            #更新参数
            w_0 = w_0 - alpha * loss * classLabels[x]
            for i in range(n):
                if dataMatrix[x, i] != 0:
                    w[i, 0] = w[i, 0] - alpha * loss * classLabels[x] * dataMatrix[x, i]
                    for j in range(k):
                        v[i, j] = v[i, j] - alpha * loss * classLabels[x] * (dataMatrix[x, i] * inter_1[0, j] - v[i, j] * dataMatrix[x, i] * dataMatrix[x, i])
        print('the no %s times, the loss arrach %s' %(it,loss_res))
    return w_0, w, v

def getAccuracy(dataMatrix, classLabels, w_0, w, v):
    m, n = shape(dataMatrix)
    allItem = 0
    error = 0
    result = []
    for x in range(m):
        allItem += 1
        inter_1 = dataMatrix[x] * v
        inter_2 = multiply(dataMatrix[x], dataMatrix[x]) * multiply(v, v)#multiply对应元素相乘
        #完成交叉项
        interaction = sum(multiply(inter_1, inter_1) - inter_2) / 2.
        p = w_0 + dataMatrix[x] * w + interaction#计算预测的输出
        pre = sigmoid(p[0, 0])
        result.append(pre)
        if pre < 0.5 and classLabels[x] == 1.0:
            error += 1
        elif pre >= 0.5 and classLabels[x] == -1.0:
            error += 1
        else:
            continue
    #print(result)
    return float(error) / allItem
        
   
if __name__ == '__main__':
    trainData = sys.argv[1]
    dataTrain, labelTrain = loadDataSet(trainData)
    #dataTest, labelTest = loadDataSet(testData)
    date_startTrain = datetime.now()
    print("开始训练")
    w_0, w, v = stocGradAscent(mat(dataTrain), labelTrain, 20, 200)
    print("训练准确性为：%f" % (1 - getAccuracy(mat(dataTrain), labelTrain, w_0, w, v)))
    date_endTrain = datetime.now()
    print("训练时间为：%s" % (date_endTrain - date_startTrain))
    print("开始测试")
    #print("测试准确性为：%f" % (1 - getAccuracy(mat(dataTest), labelTest, w_0, w, v)))
