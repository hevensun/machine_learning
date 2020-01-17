# __author__ : slade
# __time__ : 17/12/21


# model tuning step:
import pandas as pd
import numpy as np
from xgboost.sklearn import XGBClassifier
import random
from sklearn.ensemble import GradientBoostingClassifier

# load data
X_train = pd.read_csv('ensemble_X_train.csv').iloc[:, 1:]
Y_train = pd.read_csv('ensemble_Y_train.csv', header=None).iloc[:, 1:]
X_test = pd.read_csv('ensemble_X_test.csv').iloc[:, 1:]
Y_test = pd.read_csv('ensemble_Y_test.csv', header=None).iloc[:, 1:]
Y_train = np.array(Y_train).ravel()
Y_test = np.array(Y_test).ravel()


# define the evaluation criterion, the res1 is the positive case rate , the res2 is the correction rate
def metrics_spec(actual_data, predict_data, cutoff=0.5):
    actual_data = np.array(actual_data)
    predict_data = np.array(predict_data)
    bind_data = np.c_[actual_data, predict_data]
    target_rate = 1.0 * (bind_data[bind_data[:, 0] == 1][:, 1] >= cutoff).sum() / bind_data[bind_data[:, 0] == 1].shape[
        0]
    recall = 1.0 * (bind_data[bind_data[:, 0] == 1][:, 1] >= cutoff).sum() / (
        (bind_data[bind_data[:, 0] == 1][:, 1] >= cutoff).sum() +
        (bind_data[bind_data[:, 0] == 0][:, 1] <= cutoff).shape[
            0])
    accuracy = 1.0 * (
        (bind_data[bind_data[:, 0] == 1][:, 1] >= cutoff).sum() + (
            bind_data[bind_data[:, 0] == 0][:, 1] < cutoff).sum()) / \
               bind_data.shape[0]
    print('target_rate is %s' % target_rate)
    print('recall is %s' % recall)
    print('accuracy is %s' % accuracy)


# if you have read the article 'Kaggle-TianChi分类问题相关纯算法理论剖析', you may know that the bagging models need the sub_models low bias and Mutual independence
# so we should tuning for low bias and sample for Mutual independence
# limited to the time，i will show the tuning at Stacking_gbdt_logistic_regression and Stacking_xgboost_logistic_regression , this codes will skip these steps but they are quite important


# bagging case 1: use three single xgboost merge into a bagging model : (merged)xgboosts
# sample for mutual independence
# cases sample
n_index_num = list(range(X_train.shape[0]))
random.shuffle(n_index_num)
break_point = int(len(n_index_num) * 0.7)
train_index = n_index_num[:break_point]
X_train_xgb_1 = X_train.iloc[train_index, :]
Y_train_xgb_1 = Y_train[train_index]
random.shuffle(n_index_num)
break_point = int(len(n_index_num) * 0.5)
train_index = n_index_num[:break_point]
X_train_xgb_2 = X_train.iloc[train_index, :]
Y_train_xgb_2 = Y_train[train_index]
random.shuffle(n_index_num)
break_point = int(len(n_index_num) * 0.6)
train_index = n_index_num[:break_point]
X_train_xgb_3 = X_train.iloc[train_index, :]
Y_train_xgb_3 = Y_train[train_index]

# features sample
feature_num = list(range(X_train_xgb_1.shape[1]))
random.shuffle(feature_num)
X_train_xgb_1 = X_train_xgb_1.iloc[:, feature_num[:int(len(feature_num) * 0.8)]]
random.shuffle(feature_num)
X_train_xgb_2 = X_train_xgb_2.iloc[:, feature_num[:int(len(feature_num) * 0.8)]]
random.shuffle(feature_num)
X_train_xgb_3 = X_train_xgb_3.iloc[:, feature_num[:int(len(feature_num) * 0.8)]]

# warn again, you should train each model carefully here ,i skip these for cutting length of the code
clf1 = XGBClassifier(
    learning_rate=0.01,
    n_estimators=100,
    objective='binary:logistic'
)
clf2 = XGBClassifier(
    learning_rate=0.02,
    n_estimators=100,
    objective='binary:logistic'
)
clf3 = XGBClassifier(
    learning_rate=0.03,
    n_estimators=100,
    objective='binary:logistic'
)
# train the values
model_xgbs_1 = clf1.fit(X_train_xgb_1, Y_train_xgb_1)
model_xgbs_2 = clf2.fit(X_train_xgb_2, Y_train_xgb_2)
model_xgbs_3 = clf3.fit(X_train_xgb_3, Y_train_xgb_3)
y_xgbs_1 = model_xgbs_1.predict_proba(X_test[X_train_xgb_1.columns])[:, 1]
y_xgbs_2 = model_xgbs_2.predict_proba(X_test[X_train_xgb_2.columns])[:, 1]
y_xgbs_3 = model_xgbs_3.predict_proba(X_test[X_train_xgb_3.columns])[:, 1]
metrics_spec(Y_test, y_xgbs_1)
metrics_spec(Y_test, y_xgbs_2)
metrics_spec(Y_test, y_xgbs_3)

# here merge models sample by mean , you can choose other ways like correction rate、importance came out by your tree models or any rank weights you define
y_xgbs = (y_xgbs_1 + y_xgbs_2 + y_xgbs_3) / 3
metrics_spec(Y_test, y_xgbs)

# bagging case 2:the same way to train the (merged)gbdts , so i skip the annotation here
n_index_num = list(range(X_train.shape[0]))
random.shuffle(n_index_num)
break_point = int(len(n_index_num) * 0.7)
train_index = n_index_num[:break_point]
X_train_gbdt_1 = X_train.iloc[train_index, :]
Y_train_gbdt_1 = Y_train[train_index]
random.shuffle(n_index_num)
break_point = int(len(n_index_num) * 0.6)
train_index = n_index_num[:break_point]
X_train_gbdt_2 = X_train.iloc[train_index, :]
Y_train_gbdt_2 = Y_train[train_index]
random.shuffle(n_index_num)
break_point = int(len(n_index_num) * 0.5)
train_index = n_index_num[:break_point]
X_train_gbdt_3 = X_train.iloc[train_index, :]
Y_train_gbdt_3 = Y_train[train_index]

feature_num = list(range(X_train_gbdt_1.shape[1]))
random.shuffle(feature_num)
X_train_gbdt_1 = X_train_gbdt_1.iloc[:, feature_num[:int(len(feature_num) * 0.8)]]
random.shuffle(feature_num)
X_train_gbdt_2 = X_train_gbdt_2.iloc[:, feature_num[:int(len(feature_num) * 0.8)]]
random.shuffle(feature_num)
X_train_gbdt_3 = X_train_gbdt_3.iloc[:, feature_num[:int(len(feature_num) * 0.8)]]

# warn again, you should train each model carefully here ,i skip these for cutting length of the code
gbdt1 = GradientBoostingClassifier(
    loss='deviance'
    , learning_rate=0.01
    , n_estimators=100
)
gbdt2 = GradientBoostingClassifier(
    loss='deviance'
    , learning_rate=0.02
    , n_estimators=100
)
gbdt3 = GradientBoostingClassifier(
    loss='deviance'
    , learning_rate=0.04
    , n_estimators=100
)
# train the values
model_gbdt_1 = gbdt1.fit(X_train_gbdt_1, Y_train_gbdt_1)
model_gbdt_2 = gbdt2.fit(X_train_gbdt_2, Y_train_gbdt_2)
model_gbdt_3 = gbdt3.fit(X_train_gbdt_3, Y_train_gbdt_3)
y_gbdts_1 = model_gbdt_1.predict_proba(X_test[X_train_gbdt_1.columns])[:, 1]
y_gbdts_2 = model_gbdt_2.predict_proba(X_test[X_train_gbdt_2.columns])[:, 1]
y_gbdts_3 = model_gbdt_3.predict_proba(X_test[X_train_gbdt_3.columns])[:, 1]
metrics_spec(Y_test, y_gbdts_1)
metrics_spec(Y_test, y_gbdts_2)
metrics_spec(Y_test, y_gbdts_3)
y_gbdts = (y_gbdts_1 + y_gbdts_2 + y_gbdts_3) / 3
metrics_spec(Y_test, y_gbdts)


# bagging case 3:
# what's more,we can also merge the bagging models into anther bagging model such as (merged)gboosts + (merged)gdbts
for i in range(1, 10):
    rate = i / 10.0
    merge_rate = y_xgbs * rate + y_gbdts * (1 - rate)
    result = metrics_spec(Y_test, merge_rate)
    print('the %s xgboost add the %s gbdt' % (rate, 1 - rate))
    print(result)

rate = 0.9
merge_prob = y_xgbs * rate + y_gbdts * (1 - rate)
ks_gbdt_xgboost_merge = np.c_[Y_test, merge_prob]
ks_gbdt_xgboost_merge = sorted(ks_gbdt_xgboost_merge, key=lambda x: x[1], reverse=True)
ks_gbdt_xgboost_merge = pd.DataFrame(ks_gbdt_xgboost_merge)
break_cut = int(ks_gbdt_xgboost_merge.shape[0] / 10)
for i in range(9):
    end = (i + 1) * break_cut
    res1 = 1.0 * ks_gbdt_xgboost_merge.iloc[:end, :][ks_gbdt_xgboost_merge.iloc[:end, 0] == 0].shape[0] / \
           ks_gbdt_xgboost_merge[ks_gbdt_xgboost_merge.iloc[:, 0] == 0].shape[0]
    res2 = 1.0 * ks_gbdt_xgboost_merge.iloc[:end, :][ks_gbdt_xgboost_merge.iloc[:end, 0] == 1].shape[0] / \
           ks_gbdt_xgboost_merge[ks_gbdt_xgboost_merge.iloc[:, 0] == 1].shape[0]
    res = res2 - res1
    print(res1, res2, res)


    # 算法评估KS值
    # ks_gbdts = np.c_[Y_test,y_gbdts]
    # ks_gbdts = sorted(ks_gbdts , key = lambda x : x[1],reverse = True)
    # ks_gbdts = pd.DataFrame(ks_gbdts)
    # break_cut = int(ks_gbdts.shape[0]/10)
    # for i in range(9):
    # 	end = (i+1)*break_cut
    # 	res1 = 1.0*ks_gbdts.iloc[:end,:][ks_gbdts.iloc[:end,0]==0].shape[0]/ks_gbdts[ks_gbdts.iloc[:,0]==0].shape[0]
    # 	res2 = 1.0*ks_gbdts.iloc[:end,:][ks_gbdts.iloc[:end,0]==1].shape[0]/ks_gbdts[ks_gbdts.iloc[:,0]==1].shape[0]
    # 	res = res2-res1
    # 	print(res1,res2,res)
