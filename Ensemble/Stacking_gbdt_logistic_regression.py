# __author__ : slade
# __time__ : 17/12/21

import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder
from sklearn.linear_model.logistic import LogisticRegression
from sklearn.grid_search import GridSearchCV
from sklearn.ensemble import GradientBoostingClassifier

# load data
X_train = pd.read_csv('ensemble_X_train.csv').iloc[:, 1:]
Y_train = pd.read_csv('ensemble_Y_train.csv', header=None).iloc[:, 1:]
X_test = pd.read_csv('ensemble_X_test.csv').iloc[:, 1:]
Y_test = pd.read_csv('ensemble_Y_test.csv', header=None).iloc[:, 1:]
Y_train = np.array(Y_train).ravel()
Y_test = np.array(Y_test).ravel()


# define the correction rate , the res1 is the positive case rate , the res2 is the correction rate
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


# if you have read the article 'Kaggle-TianChi分类问题相关纯算法理论剖析', you may know the suggestion of tuning methods , let's follow

# get the base line first
gbm0 = GradientBoostingClassifier(random_state=10)
gbm0.fit(X_train, Y_train)
y_predprob = gbm0.predict_proba(X_test)[:, 1]
metrics_spec(Y_test, y_predprob)

# get the n_estimators and learning_rate ,but here is gbdt , only n_estimators
# if necessary ,increasing param:cv can increase the confidence degree of the current model's result
param_test1 = {'n_estimators': [10, 50, 100, 300, 500]}
gsearch1 = GridSearchCV(estimator=GradientBoostingClassifier(random_state=10),
                        param_grid=param_test1, scoring='roc_auc', iid=False, cv=2)
gsearch1.fit(X_train, Y_train)
print(gsearch1.best_params_)
# {'n_estimators': 50}

# get subsample next
param_test2 = {'subsample': [0.7, 0.8, 0.9, 1]}
gsearch2 = GridSearchCV(estimator=GradientBoostingClassifier(n_estimators=50, random_state=10),
                        param_grid=param_test2, scoring='roc_auc', iid=False, cv=2)
gsearch2.fit(X_train, Y_train)
print(gsearch2.best_params_)
# first show like {'subsample': 0.7},so we need reset the init subsample
# param_test2 = {'subsample': [0.5, 0.6, 0.7]}
# gsearch2 = GridSearchCV(estimator=GradientBoostingClassifier(n_estimators=50, random_state=10),
#                         param_grid=param_test2, scoring='roc_auc', iid=False, cv=2)
# gsearch2.fit(X_train, Y_train)
# print(gsearch2.best_params_)
# {'subsample': 0.6}

# i have train the max_leaf_nodes and min_weight_fraction_leaf privately but it doesn't work ,so we skip it.Get min_samples_split and max_depth result directly
param_test3 = {'min_samples_split': [400, 900, 1300],
               'max_depth': [3, 5, 7, 9]
               }
gsearch3 = GridSearchCV(
    estimator=GradientBoostingClassifier(n_estimators=50, random_state=10, subsample=0.6),
    param_grid=param_test3, scoring='roc_auc', iid=False, cv=2)
gsearch3.fit(X_train, Y_train)
print(gsearch3.best_params_)
# {'max_depth': 7, 'min_samples_split': 900}

# for short, we skip the process of training the max_features and '鞍点逃逸' and '极限探索',but if u want to train a nice model these ways should be added at your process
# to be frank ,it takes to much time
gbm1 = GradientBoostingClassifier(n_estimators=50, random_state=10, subsample=0.6, max_depth=7,
                                  min_samples_split=900)
gbm1.fit(X_train, Y_train)
y_predprob = gbm1.predict_proba(X_test)[:, 1]
metrics_spec(Y_test, y_predprob)

# we can the get spare leaf nodes for the input of stacking
train_new_feature = gbm1.apply(X_train)
test_new_feature = gbm1.apply(X_test)
train_new_feature = train_new_feature.reshape(-1, 50)
test_new_feature = test_new_feature.reshape(-1, 50)
enc = OneHotEncoder()
enc.fit(train_new_feature)
train_new_feature2 = np.array(enc.transform(train_new_feature).toarray())
test_new_feature2 = np.array(enc.transform(test_new_feature).toarray())

# stacking a model , it can be logisticRegression or fm, nerual network and they will come to be beyond all expectations
# attention points of the stacking model can be obtained from the article mentioned at the top of the code
lr = LogisticRegression(C=1, penalty='l1', max_iter=100, solver='liblinear', multi_class='ovr')
model_lr = lr.fit(train_new_feature2, Y_train)
y_test_lr = model_lr.predict_proba(test_new_feature2)[:, 1]
res2 = metrics_spec(Y_test, y_test_lr)
