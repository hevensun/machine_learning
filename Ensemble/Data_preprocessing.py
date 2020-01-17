# __author__ : slade
# __time__ : 17/12/21

import pandas as pd
import numpy as np
from xgboost.sklearn import XGBClassifier
import random
from data_preprocessing import data_preprocessing
from sklearn.externals import joblib

# load data
path1 = 'ensemble_data.txt'
train_data = pd.read_table(path1)
# change columns
train_data.columns = ['uid', 'label', 'f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9', 'f10', 'f11', 'f12', 'f13',
                      'f14', 'f15', 'f16', 'f17', 'f18', 'f19', 'f20', 'f21', 'f22', 'f23', 'f24', 'f25', 'f26', 'f27',
                      'f28', 'f29', 'f30', 'f31', 'f32', 'f33', 'f34', 'f35', 'f36', 'f37', 'f38', 'f39', 'f40', 'f41',
                      'f42', 'f43', 'f44', 'f45', 'f46', 'f47', 'f48', 'f49', 'f50', 'f51', 'f52', 'f53', 'f54', 'f55',
                      'f56', 'f57', 'f58', 'f59', 'f60', 'f61', 'f62', 'f63', 'f64', 'f65', 'f66', 'f67', 'f68', 'f69',
                      'f70', 'f71', 'f72', 'f73', 'f74', 'f75', 'f76', 'f77', 'f78', 'f79', 'f80', 'f81', 'f82', 'f83',
                      'f84', 'f85', 'f86', 'f87', 'f88', 'f89', 'f90', 'f91', 'f92', 'f93', 'f94', 'f95', 'f96', 'f97',
                      'f98', 'f99', 'f100', 'f101', 'f102', 'f103', 'f104', 'f105', 'f106', 'f107', 'f108', 'f109',
                      'f110']

# describe every columns
# the different element number of every column
arrange_data_col = {}
# the different element of every column
detail_data_col = {}
for i in train_data.columns:
    if i != 'uid':
        arrange_data_col[i] = len(set(train_data[i]))
        detail_data_col[i] = set(train_data[i])

# separate the classification data : define that if the set is under 10,the columns can be treated as classification,you can also change the number 10 to any number you need
# the class columns set
class_set = []
# the continue columns set
continue_set = []
for key in arrange_data_col:
    if arrange_data_col[key] >= 10 and key != 'uid':
        continue_set.append(key)

class_set = [x for x in train_data.columns if
             x not in continue_set and x != 'uid' and x != 'label' and arrange_data_col[x] > 1]

# make the continuous data
continue_reshape_train_data = train_data[continue_set][:]


# remove the null columns here ,but i do not use this function,you can try it
def continuous_columns_nan_count(data, columns):
    res = []
    for i in columns:
        rate = (data[i] < 0).sum() / data[i].shape[0]
        res.append((i, rate))
        print('we have got the %s' % i)
    return res


continue_describe = continuous_columns_nan_count(continue_reshape_train_data, continue_set)
continue_set_classed = [x[0] for x in continue_describe]
continue_set_classed_data = pd.DataFrame()
keep_q_set = {}
# split continuous columns into 10 sub_class columns
for i in continue_set_classed:
    assistant_vector = []
    q1 = continue_reshape_train_data[i][continue_reshape_train_data[i] != -1].quantile(0.1)
    q2 = continue_reshape_train_data[i][continue_reshape_train_data[i] != -1].quantile(0.2)
    q3 = continue_reshape_train_data[i][continue_reshape_train_data[i] != -1].quantile(0.3)
    q4 = continue_reshape_train_data[i][continue_reshape_train_data[i] != -1].quantile(0.4)
    q5 = continue_reshape_train_data[i][continue_reshape_train_data[i] != -1].quantile(0.5)
    q6 = continue_reshape_train_data[i][continue_reshape_train_data[i] != -1].quantile(0.6)
    q7 = continue_reshape_train_data[i][continue_reshape_train_data[i] != -1].quantile(0.7)
    q8 = continue_reshape_train_data[i][continue_reshape_train_data[i] != -1].quantile(0.8)
    q9 = continue_reshape_train_data[i][continue_reshape_train_data[i] != -1].quantile(0.9)
    q_set = set([q1, q2, q3, q4, q5, q6, q7, q8, q9])
    keep_q_set[i] = q_set
    if len(q_set) == 9:
        array_q_set = [x for x in q_set]
        for j in range(continue_reshape_train_data[i].shape[0]):
            if continue_reshape_train_data[i][j] == -1:
                assistant_vector.append(-1)
            elif continue_reshape_train_data[i][j] <= array_q_set[0]:
                assistant_vector.append(0)
            elif continue_reshape_train_data[i][j] <= array_q_set[1]:
                assistant_vector.append(1)
            elif continue_reshape_train_data[i][j] <= array_q_set[2]:
                assistant_vector.append(2)
            elif continue_reshape_train_data[i][j] <= array_q_set[3]:
                assistant_vector.append(3)
            elif continue_reshape_train_data[i][j] <= array_q_set[4]:
                assistant_vector.append(4)
            elif continue_reshape_train_data[i][j] <= array_q_set[5]:
                assistant_vector.append(5)
            elif continue_reshape_train_data[i][j] <= array_q_set[6]:
                assistant_vector.append(6)
            elif continue_reshape_train_data[i][j] <= array_q_set[7]:
                assistant_vector.append(7)
            elif continue_reshape_train_data[i][j] <= array_q_set[8]:
                assistant_vector.append(8)
            else:
                assistant_vector.append(9)
    if len(q_set) == 8:
        array_q_set = [x for x in q_set]
        for j in range(continue_reshape_train_data[i].shape[0]):
            if continue_reshape_train_data[i][j] == -1:
                assistant_vector.append(-1)
            elif continue_reshape_train_data[i][j] <= array_q_set[0]:
                assistant_vector.append(0)
            elif continue_reshape_train_data[i][j] <= array_q_set[1]:
                assistant_vector.append(1)
            elif continue_reshape_train_data[i][j] <= array_q_set[2]:
                assistant_vector.append(2)
            elif continue_reshape_train_data[i][j] <= array_q_set[3]:
                assistant_vector.append(3)
            elif continue_reshape_train_data[i][j] <= array_q_set[4]:
                assistant_vector.append(4)
            elif continue_reshape_train_data[i][j] <= array_q_set[5]:
                assistant_vector.append(5)
            elif continue_reshape_train_data[i][j] <= array_q_set[6]:
                assistant_vector.append(6)
            elif continue_reshape_train_data[i][j] <= array_q_set[7]:
                assistant_vector.append(7)
            else:
                assistant_vector.append(8)
    if len(q_set) == 7:
        array_q_set = [x for x in q_set]
        for j in range(continue_reshape_train_data[i].shape[0]):
            if continue_reshape_train_data[i][j] == -1:
                assistant_vector.append(-1)
            elif continue_reshape_train_data[i][j] <= array_q_set[0]:
                assistant_vector.append(0)
            elif continue_reshape_train_data[i][j] <= array_q_set[1]:
                assistant_vector.append(1)
            elif continue_reshape_train_data[i][j] <= array_q_set[2]:
                assistant_vector.append(2)
            elif continue_reshape_train_data[i][j] <= array_q_set[3]:
                assistant_vector.append(3)
            elif continue_reshape_train_data[i][j] <= array_q_set[4]:
                assistant_vector.append(4)
            elif continue_reshape_train_data[i][j] <= array_q_set[5]:
                assistant_vector.append(5)
            elif continue_reshape_train_data[i][j] <= array_q_set[6]:
                assistant_vector.append(6)
            else:
                assistant_vector.append(7)
    if len(q_set) == 6:
        array_q_set = [x for x in q_set]
        for j in range(continue_reshape_train_data[i].shape[0]):
            if continue_reshape_train_data[i][j] == -1:
                assistant_vector.append(-1)
            elif continue_reshape_train_data[i][j] <= array_q_set[0]:
                assistant_vector.append(0)
            elif continue_reshape_train_data[i][j] <= array_q_set[1]:
                assistant_vector.append(1)
            elif continue_reshape_train_data[i][j] <= array_q_set[2]:
                assistant_vector.append(2)
            elif continue_reshape_train_data[i][j] <= array_q_set[3]:
                assistant_vector.append(3)
            elif continue_reshape_train_data[i][j] <= array_q_set[4]:
                assistant_vector.append(4)
            elif continue_reshape_train_data[i][j] <= array_q_set[5]:
                assistant_vector.append(5)
            else:
                assistant_vector.append(6)
    if len(q_set) == 5:
        array_q_set = [x for x in q_set]
        for j in range(continue_reshape_train_data[i].shape[0]):
            if continue_reshape_train_data[i][j] == -1:
                assistant_vector.append(-1)
            elif continue_reshape_train_data[i][j] <= array_q_set[0]:
                assistant_vector.append(0)
            elif continue_reshape_train_data[i][j] <= array_q_set[1]:
                assistant_vector.append(1)
            elif continue_reshape_train_data[i][j] <= array_q_set[2]:
                assistant_vector.append(2)
            elif continue_reshape_train_data[i][j] <= array_q_set[3]:
                assistant_vector.append(3)
            elif continue_reshape_train_data[i][j] <= array_q_set[4]:
                assistant_vector.append(4)
            else:
                assistant_vector.append(5)
    if len(q_set) == 4:
        array_q_set = [x for x in q_set]
        for j in range(continue_reshape_train_data[i].shape[0]):
            if continue_reshape_train_data[i][j] == -1:
                assistant_vector.append(-1)
            elif continue_reshape_train_data[i][j] <= array_q_set[0]:
                assistant_vector.append(0)
            elif continue_reshape_train_data[i][j] <= array_q_set[1]:
                assistant_vector.append(1)
            elif continue_reshape_train_data[i][j] <= array_q_set[2]:
                assistant_vector.append(2)
            elif continue_reshape_train_data[i][j] <= array_q_set[3]:
                assistant_vector.append(3)
            else:
                assistant_vector.append(4)
    if len(q_set) == 3:
        array_q_set = [x for x in q_set]
        for j in range(continue_reshape_train_data[i].shape[0]):
            if continue_reshape_train_data[i][j] == -1:
                assistant_vector.append(-1)
            elif continue_reshape_train_data[i][j] <= array_q_set[0]:
                assistant_vector.append(0)
            elif continue_reshape_train_data[i][j] <= array_q_set[1]:
                assistant_vector.append(1)
            elif continue_reshape_train_data[i][j] <= array_q_set[2]:
                assistant_vector.append(2)
            else:
                assistant_vector.append(3)
    if len(q_set) == 2:
        array_q_set = [x for x in q_set]
        for j in range(continue_reshape_train_data[i].shape[0]):
            if continue_reshape_train_data[i][j] == -1:
                assistant_vector.append(-1)
            elif continue_reshape_train_data[i][j] <= min(array_q_set):
                assistant_vector.append(0)
            elif continue_reshape_train_data[i][j] <= max(array_q_set):
                assistant_vector.append(1)
            else:
                assistant_vector.append(2)
    if len(q_set) == 1:
        array_q_set = [x for x in q_set]
        for j in range(continue_reshape_train_data[i].shape[0]):
            if continue_reshape_train_data[i][j] == -1:
                assistant_vector.append(-1)
            elif continue_reshape_train_data[i][j] <= min(array_q_set):
                assistant_vector.append(0)
            else:
                assistant_vector.append(1)
    if len(q_set) == 0:
        assistant_vector = [-1] * continue_reshape_train_data[i].shape[0]
    continue_set_classed_data = pd.concat([continue_set_classed_data, pd.DataFrame(assistant_vector)], axis=1)
    print('we have got the continuous column : %s ' % i)

# save the quantiles of each columns, you will load them if u want to deploy a trained model
joblib.dump(keep_q_set, 'keep_q_set.pkl')

# merge the data
continue_set_classed_data.columns = continue_set_classed
cbind_classed_data_columns = continue_set_classed + class_set
cbind_classed_data = pd.concat(
    [train_data['uid'], train_data['label'], continue_set_classed_data, train_data[class_set]], axis=1)

# describe every columns again for removing the low variance columns
arrange_data_col = {}
detail_data_col = {}
for i in cbind_classed_data_columns:
    if i != 'uid' and i != 'label':
        arrange_data_col[i] = len(set(cbind_classed_data[i]))
        detail_data_col[i] = set(cbind_classed_data[i])

# I do not use this function , if needed ,try it
meaningful_col = ['uid', 'label']
for i in cbind_classed_data_columns:
    if i != 'uid' and i != 'label':
        if arrange_data_col[i] >= 2:
            meaningful_col.append(i)
meaningful_data = cbind_classed_data[meaningful_col]

# reshape the merged data and oht the data
reshaped_data = pd.DataFrame()
for i in meaningful_col:
    if i != 'uid' and i != 'label':
        reshaped_data = pd.concat([reshaped_data, pd.get_dummies(meaningful_data[i], prefix=i)], axis=1)
        print('we have got the classification column %s ' % i)
reshaped_data = pd.concat(
    [cbind_classed_data['uid'], cbind_classed_data['label'], reshaped_data], axis=1)

# feature_filter , remove the useless columns by Mutual Information
ff = data_preprocessing.feature_filter()
res = ff.mic_entroy(reshaped_data.iloc[:, 1:], 'label')


# define the evaluation criterion, the res1 is the positive case rate , the res2 is the correction rate
def metrics_spec(actual_data, predict_data, cutoff=0.5):
    actual_data = np.array(actual_data)
    predict_data = np.array(predict_data)
    bind_data = np.c_[actual_data, predict_data]
    res1 = 1.0 * (bind_data[bind_data[:, 0] == 1][:, 1] >= cutoff).sum() / bind_data[bind_data[:, 0] == 1].shape[0]
    res2 = 1.0 * (
        (bind_data[bind_data[:, 0] == 1][:, 1] >= cutoff).sum() + (
            bind_data[bind_data[:, 0] == 0][:, 1] < cutoff).sum()) / \
           bind_data.shape[0]
    return res1, res2


# define the initial tree param ,remove the useless columns by the importance in xgboost
clf = XGBClassifier(
    learning_rate=0.01,
    n_estimators=500,
    objective='binary:logistic',
)

# best cutoff : 223 , train it with your data by yourself
filter_columns = ['uid', 'label'] + [x[0] for x in res[-223:]]
reshaped_data = reshaped_data[filter_columns]
X_train = reshaped_data.iloc[:, 2:]
y_train = reshaped_data.iloc[:, 1]
model_sklearn = clf.fit(X_train, y_train)

# calculate the importance ,best cutoff : 0.0022857142612338 , train it with your data by yourself
importance = np.c_[X_train.columns, model_sklearn.feature_importances_]
train_columns = [x[0] for x in importance if x[1] > 0.0022857142612338]
# save the train columns, you will load them if u want to deploy a trained model
joblib.dump(train_columns, 'train_columns.pkl')
train_columns = list(reshaped_data.columns[:2]) + train_columns

# make train&test data with 8:2
reshaped_data = reshaped_data[train_columns]
n_index_num = list(range(reshaped_data.shape[0]))
random.shuffle(n_index_num)
break_point = int(len(n_index_num) * 0.8)
train_index = n_index_num[:break_point]
test_index = n_index_num[break_point:]
X_train = reshaped_data.iloc[train_index, 2:]
Y_train = reshaped_data.iloc[train_index, 1]
X_test = reshaped_data.iloc[test_index, 2:]
Y_test = reshaped_data.iloc[test_index, 1]

# save data into local for later training
X_train.to_csv('ensemble_X_train.csv')
Y_train.to_csv('ensemble_Y_train.csv')
X_test.to_csv('ensemble_X_test.csv')
Y_test.to_csv('ensemble_Y_test.csv')
