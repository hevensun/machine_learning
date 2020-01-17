# __author__ : slade
# __time__ : 17/12/21

import pandas as pd
import numpy as np
from xgboost.sklearn import XGBClassifier
from sklearn.preprocessing import OneHotEncoder
from sklearn.linear_model.logistic import LogisticRegression
from sklearn.grid_search import GridSearchCV

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

# you can adjust scale_weight_suggestion = (len(Y_train) - Y_train.sum()) / Y_train.sum() to balance your scale between positive cases and negtive cases
# get the n_estimators and learning_rate first
# if necessary ,increasing param:cv can increase the confidence degree of the current model's result
param_test = {
    'learning_rate': [0.1, 0.3, 0.9],
    'n_estimators': [50, 100, 300, 500]
}
gsearch = GridSearchCV(
    estimator=XGBClassifier(
        learning_rate=0.1,
        objective='binary:logistic',
        scale_pos_weight=1.002252816020025,
        seed=27),
    param_grid=param_test,
    scoring='roc_auc',
    n_jobs=4,
    iid=False,
    cv=2)
gsearch.fit(X_train, Y_train)
print(gsearch.best_params_)
# {'learning_rate': 0.1, 'n_estimators': 100}
# we should also consider the training speed of each process,sometimes we can sacrifice some effect to improve the speed. but don't worry , you can also retrain the two param at last if needed


# get subsample next
param_test1 = {
    'subsample': [0.6, 0.7, 0.8, 0.9]
}
gsearch1 = GridSearchCV(
    estimator=XGBClassifier(
        learning_rate=0.1,
        n_estimators=100,
        objective='binary:logistic',
        scale_pos_weight=1.002252816020025,
        seed=27),
    param_grid=param_test1,
    scoring='roc_auc',
    n_jobs=4,
    iid=False,
    cv=2)
gsearch1.fit(X_train, Y_train)
print(gsearch1.best_params_)
# {'subsample': 0.7}

# if you want your model more accurate , you can calculate the accuration at your test set after each training process
# Compared with the last time at your test set if the accuracy rate decline, you should follow actions from the article guide 'Kaggle-TianChi分类问题相关纯算法理论剖析' to adjust the params

# i have train the max_leaf_nodes and min_weight_fraction_leaf privately but it doesn't work ,so we skip it. get min_samples_split and max_depth result directly
param_test2 = {
    'max_depth': [3, 5, 7],
    'min_child_weight': [0.8, 1, 1.2]

}
gsearch2 = GridSearchCV(
    estimator=XGBClassifier(
        learning_rate=0.1,
        n_estimators=100,
        subsample=0.7,
        objective='binary:logistic',
        scale_pos_weight=1.002252816020025,
        seed=27),
    param_grid=param_test2,
    scoring='roc_auc',
    n_jobs=4,
    iid=False,
    cv=2)
gsearch2.fit(X_train, Y_train)
print(gsearch2.best_params_)
# {'max_depth': 3, 'min_child_weight': 0.8}

# train colsample_bytree next
param_test3 = {
    'colsample_bytree': [0.6, 0.7, 0.8, 0.9]
}
gsearch3 = GridSearchCV(
    estimator=XGBClassifier(
        learning_rate=0.1,
        n_estimators=100,
        max_depth=3,
        subsample=0.8,
        min_child_weight=0.7,
        objective='binary:logistic',
        scale_pos_weight=1.002252816020025,
        seed=27),
    param_grid=param_test3,
    scoring='roc_auc',
    n_jobs=4,
    iid=False,
    cv=2)
gsearch3.fit(X_train, Y_train)
print(gsearch3.best_params_)
# {'colsample_bytree': 0.7}

# reg_lambda and reg_alpha at last
param_test4 = {
    'reg_lambda': [0.1, 0.3, 0.9, 3],
    'reg_alpha': [0.1, 0.3, 0.9, 3]
}
gsearch4 = GridSearchCV(
    estimator=XGBClassifier(
        learning_rate=0.1,
        n_estimators=100,
        max_depth=3,
        subsample=0.7,
        min_child_weight=0.8,
        colsample_bytree=0.7,
        objective='binary:logistic',
        scale_pos_weight=1.002252816020025,
        seed=27),
    param_grid=param_test4,
    scoring='roc_auc',
    n_jobs=4,
    iid=False,
    cv=2)
gsearch4.fit(X_train, Y_train)
print(gsearch4.best_params_)
# {'reg_alpha': 0.3, 'reg_lambda': 0.1}


# for short, we skip the process of training the max_features and the process of training the pairs between learning_rate and n_estimators,but if u want to train a nice model these ways should be added at your process.
# with the same reason，i skip the code '鞍点逃逸' and '极限探索' ,follow the methods mentioned at the article 'Kaggle&TianChi分类问题相关纯算法理论剖析' ,try it by yourself

# define the final param
clf = XGBClassifier(
    learning_rate=0.1,
    n_estimators=100,
    max_depth=3,
    subsample=0.7,
    min_child_weight=0.8,
    colsample_bytree=0.7,
    objective='binary:logistic',
    scale_pos_weight=1.002252816020025,
    reg_alpha=0.3,
    reg_lambda=0.1,
    seed=27
)

# train the values
model_sklearn = clf.fit(X_train, Y_train)
y_bst = model_sklearn.predict_proba(X_test)[:, 1]
metrics_spec(Y_train, model_sklearn.predict_proba(X_train)[:, 1])
metrics_spec(Y_test, y_bst)

# make new features
# we can get the spare leaf nodes for the input of stacking
train_new_feature = clf.apply(X_train)
test_new_feature = clf.apply(X_test)
enc = OneHotEncoder()
enc.fit(train_new_feature)
train_new_feature2 = np.array(enc.transform(train_new_feature).toarray())
test_new_feature2 = np.array(enc.transform(test_new_feature).toarray())
res_data = pd.DataFrame(np.c_[Y_train, train_new_feature2])
res_data.columns = ['f' + str(x) for x in range(res_data.shape[1])]
res_test = pd.DataFrame(np.c_[Y_test, test_new_feature2])
res_test.columns = ['f' + str(x) for x in range(res_test.shape[1])]

# stacking a model , it can be logistic or fm, nerual network and they  will come to be beyond all expectations
# attention points of the stacking model can be obtained from the article mentioned at the top of the code
lr = LogisticRegression(C=1, penalty='l2', max_iter=100, solver='sag', multi_class='ovr')
model_lr = lr.fit(res_data.iloc[:, 1:], res_data['f0'])
y_train_lr = model_lr.predict_proba(res_data.iloc[:, 1:])[:, 1]
y_test_lr = model_lr.predict_proba(res_test.iloc[:, 1:])[:, 1]
res = metrics_spec(Y_test, y_test_lr)
correct_rank = X_train.columns



# save models, you will load them if u want to deploy a trained model
from sklearn.externals import joblib

joblib.dump(model_sklearn, 'model_sklearn.pkl')
joblib.dump(correct_rank, 'correct_rank.pkl')
joblib.dump(enc, 'enc.pkl')
joblib.dump(model_lr, 'model_lr.pkl')



# 算法评估 ks值
# ks_xgb_lr = np.c_[Y_test,y_test_lr]
# ks_xgb_lr = sorted(ks_xgb_lr , key = lambda x : x[1],reverse = True)
# ks_xgb_lr = pd.DataFrame(ks_xgb_lr)
# for i in range(9):
# 	end = (i+1)*break_cut
# 	res1 = 1.0*ks_xgb_lr.iloc[:end,:][ks_xgb_lr.iloc[:end,0]==0].shape[0]/ks_xgb_lr[ks_xgb_lr.iloc[:,0]==0].shape[0]
# 	res2 = 1.0*ks_xgb_lr.iloc[:end,:][ks_xgb_lr.iloc[:end,0]==1].shape[0]/ks_xgb_lr[ks_xgb_lr.iloc[:,0]==1].shape[0]
# 	res = res2-res1
# 	print(res1,res2,res)
