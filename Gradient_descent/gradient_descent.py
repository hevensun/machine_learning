#_*_ coding:utf-8 _*_
import numpy as np
import pandas as pd

__author__ = 'slade'
__date__ = '20170228'
#logistic回归下的批量梯度下降gradAscent、随机梯度下降stocgradAscent，learning_rate变化的stocgradAscent重写
risk_data=pd.read_table('/Users/slade/Documents/Yoho/personal-code/machine-learning/data/data_all.txt')
labels = np.mat(risk_data.iloc[:,1]).T
features = np.mat(risk_data.iloc[:,2:])


def sigmoid(x):
	return 1.0/(1+np.exp(-x))

def gradAscent(features,labels,learning_rate = 0.0001,esp = 0.0001,max_iter = 100000):
	n,m = features.shape
	weighets = np.ones((m,1))
	learning_rate = learning_rate
	esp = esp
	max_iter = max_iter
	for k in range(max_iter):
		value = sigmoid(features*weighets)
		diff = value - labels
		weighets = weighets - learning_rate * features.T * diff
		loss = diff.mean()
		print('the %s time(s) train is over, now the loss is %s' %(k,loss))
		if abs(loss) < esp:
			print('reach the best result')
			print(weighets)
			break
		if k == max_iter-1:
			print('reach the max iter')
			print(weighets)
	return weighets,loss


def stocgradAscent(features,labels,learning_rate = 0.0001):
	n,m = features.shape
	weighets = np.ones((m,1))
	learning_rate = learning_rate
	for i in range(len(features)):
		value = sigmoid(sum(features[i]*weighets))
		diff = value - labels[i]	
		weighets = weighets - learning_rate * features[i].T * diff
		loss = diff.mean()
		print('the %s time(s) train is over, now the loss is %s' %(i,abs(loss)))
	return weighets,loss

def stocgradAscentLreaingRate(features,labels,max_iter = 100):
	n,m = features.shape
	weighets = np.ones((m,1))
	for i in range(max_iter):
		data_index = list(range(n))
		for j in data_index:
			learning_rate = 4.0/(i+j+1) + 0.000001
			rand_index = int(np.random.uniform(0,m))
			value = sigmoid(sum(features[rand_index]*weighets))
			diff = value - labels[rand_index]
			weighets = weighets - learning_rate * features[rand_index].T * diff
			loss = diff.mean()
			del data_index[rand_index]
		print('the %s time(s) of train is over, now the loss is %s' %(i,abs(loss)))
	return weighets,loss