# __author__ : slade
# __time__ : 17/12/21
# -*- coding:utf-8 -*-
import pandas as pd
import numpy as np
import random
import sys
from sklearn.externals import joblib


# just deploy code ， nothing need to emphasize
def data_columns_arrange(data):
    train_data = data
    train_data.columns = ['uid', 'f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9', 'f10', 'f11', 'f12', 'f13',
                          'f14', 'f15', 'f16', 'f17', 'f18', 'f19', 'f20', 'f21', 'f22', 'f23', 'f24', 'f25', 'f26',
                          'f27',
                          'f28', 'f29', 'f30', 'f31', 'f32', 'f33', 'f34', 'f35', 'f36', 'f37', 'f38', 'f39', 'f40',
                          'f41',
                          'f42', 'f43', 'f44', 'f45', 'f46', 'f47', 'f48', 'f49', 'f50', 'f51', 'f52', 'f53', 'f54',
                          'f55',
                          'f56', 'f57', 'f58', 'f59', 'f60', 'f61', 'f62', 'f63', 'f64', 'f65', 'f66', 'f67', 'f68',
                          'f69',
                          'f70', 'f71', 'f72', 'f73', 'f74', 'f75', 'f76', 'f77', 'f78', 'f79', 'f80', 'f81', 'f82',
                          'f83',
                          'f84', 'f85', 'f86', 'f87', 'f88', 'f89', 'f90', 'f91', 'f92', 'f93', 'f94', 'f95', 'f96',
                          'f97',
                          'f98', 'f99', 'f100', 'f101', 'f102', 'f103', 'f104', 'f105', 'f106', 'f107', 'f108', 'f109',
                          'f110']
    return train_data


def continuous_data_splited(data, split_point):
    continue_set_classed_data = pd.DataFrame()
    for i in split_point.keys():
        assistant_vector = []
        values = [x for x in split_point[i]]
        if len(split_point[i]) == 9:
            for j in range(data[i].shape[0]):
                if data[i][j] == -1:
                    assistant_vector.append(-1)
                elif data[i][j] <= values[0]:
                    assistant_vector.append(0)
                elif data[i][j] <= values[1]:
                    assistant_vector.append(1)
                elif data[i][j] <= values[2]:
                    assistant_vector.append(2)
                elif data[i][j] <= values[3]:
                    assistant_vector.append(3)
                elif data[i][j] <= values[4]:
                    assistant_vector.append(4)
                elif data[i][j] <= values[5]:
                    assistant_vector.append(5)
                elif data[i][j] <= values[6]:
                    assistant_vector.append(6)
                elif data[i][j] <= values[7]:
                    assistant_vector.append(7)
                elif data[i][j] <= values[8]:
                    assistant_vector.append(8)
                else:
                    assistant_vector.append(9)
        if len(split_point[i]) == 8:
            for j in range(data[i].shape[0]):
                if data[i][j] == -1:
                    assistant_vector.append(-1)
                elif data[i][j] <= values[0]:
                    assistant_vector.append(0)
                elif data[i][j] <= values[1]:
                    assistant_vector.append(1)
                elif data[i][j] <= values[2]:
                    assistant_vector.append(2)
                elif data[i][j] <= values[3]:
                    assistant_vector.append(3)
                elif data[i][j] <= values[4]:
                    assistant_vector.append(4)
                elif data[i][j] <= values[5]:
                    assistant_vector.append(5)
                elif data[i][j] <= values[6]:
                    assistant_vector.append(6)
                elif data[i][j] <= values[7]:
                    assistant_vector.append(7)
                else:
                    assistant_vector.append(8)
        if len(split_point[i]) == 7:
            for j in range(data[i].shape[0]):
                if data[i][j] == -1:
                    assistant_vector.append(-1)
                elif data[i][j] <= values[0]:
                    assistant_vector.append(0)
                elif data[i][j] <= values[1]:
                    assistant_vector.append(1)
                elif data[i][j] <= values[2]:
                    assistant_vector.append(2)
                elif data[i][j] <= values[3]:
                    assistant_vector.append(3)
                elif data[i][j] <= values[4]:
                    assistant_vector.append(4)
                elif data[i][j] <= values[5]:
                    assistant_vector.append(5)
                elif data[i][j] <= values[6]:
                    assistant_vector.append(6)
                else:
                    assistant_vector.append(7)
        if len(split_point[i]) == 6:
            for j in range(data[i].shape[0]):
                if data[i][j] == -1:
                    assistant_vector.append(-1)
                elif data[i][j] <= values[0]:
                    assistant_vector.append(0)
                elif data[i][j] <= values[1]:
                    assistant_vector.append(1)
                elif data[i][j] <= values[2]:
                    assistant_vector.append(2)
                elif data[i][j] <= values[3]:
                    assistant_vector.append(3)
                elif data[i][j] <= values[4]:
                    assistant_vector.append(4)
                elif data[i][j] <= values[5]:
                    assistant_vector.append(5)
                else:
                    assistant_vector.append(6)
        if len(split_point[i]) == 5:
            for j in range(data[i].shape[0]):
                if data[i][j] == -1:
                    assistant_vector.append(-1)
                elif data[i][j] <= values[0]:
                    assistant_vector.append(0)
                elif data[i][j] <= values[1]:
                    assistant_vector.append(1)
                elif data[i][j] <= values[2]:
                    assistant_vector.append(2)
                elif data[i][j] <= values[3]:
                    assistant_vector.append(3)
                elif data[i][j] <= values[4]:
                    assistant_vector.append(4)
                else:
                    assistant_vector.append(5)
        if len(split_point[i]) == 4:
            for j in range(data[i].shape[0]):
                if data[i][j] == -1:
                    assistant_vector.append(-1)
                elif data[i][j] <= values[0]:
                    assistant_vector.append(0)
                elif data[i][j] <= values[1]:
                    assistant_vector.append(1)
                elif data[i][j] <= values[2]:
                    assistant_vector.append(2)
                elif data[i][j] <= values[3]:
                    assistant_vector.append(3)
                else:
                    assistant_vector.append(4)
        if len(split_point[i]) == 3:
            for j in range(data[i].shape[0]):
                if data[i][j] == -1:
                    assistant_vector.append(-1)
                elif data[i][j] <= values[0]:
                    assistant_vector.append(0)
                elif data[i][j] <= values[1]:
                    assistant_vector.append(1)
                elif data[i][j] <= values[2]:
                    assistant_vector.append(2)
                else:
                    assistant_vector.append(3)
        if len(split_point[i]) == 2:
            for j in range(data[i].shape[0]):
                if data[i][j] == -1:
                    assistant_vector.append(-1)
                elif data[i][j] <= values[0]:
                    assistant_vector.append(0)
                elif data[i][j] <= values[1]:
                    assistant_vector.append(1)
                else:
                    assistant_vector.append(2)
        if len(split_point[i]) == 1:
            for j in range(data[i].shape[0]):
                if data[i][j] == -1:
                    assistant_vector.append(-1)
                elif data[i][j] <= values[0]:
                    assistant_vector.append(0)
                else:
                    assistant_vector.append(1)
        continue_set_classed_data = pd.concat([continue_set_classed_data, pd.DataFrame(assistant_vector)], axis=1)
        print('we have got the continuous column : %s ' % i)
    return continue_set_classed_data


def meaningful_columns(data, columns):
    reshaped_data = pd.DataFrame()
    for i in columns:
        if i != 'uid':
            reshaped_data = pd.concat([reshaped_data, pd.get_dummies(data[i], prefix=i)], axis=1)
            print('we have got the classification column %s ' % i)
    reshaped_data = pd.concat(
        [data['uid'], reshaped_data], axis=1)
    daily_columns = columns
    return reshaped_data, daily_columns


def fill_data_with_trained(data, columns):
    already_exist = []
    not_exist = []
    df1 = pd.DataFrame()
    df2 = pd.DataFrame()
    columns = [x for x in columns]
    for i in columns:
        if i in data.columns:
            df1 = pd.concat([df1, pd.DataFrame(data[i])], axis=1)
            already_exist.append(i)
        else:
            df3 = pd.DataFrame(np.zeros((data.shape[0], 1)))
            df3.columns = [i]
            df2 = pd.concat([df2, df3], axis=1)
            not_exist.append(i)
    df = pd.concat([df1, df2], axis=1)
    return df, already_exist, not_exist


def main():
    # read data
    print('开始预测！')
    path = sys.argv[1]
    # path = 'ensemble_demp_data.txt'
    try:
        train_data = pd.read_table(path, header=None)
    except:
        raise IllegalInput(
            'Error : the wrong input path!')
    train_data = data_columns_arrange(train_data)
    keep_q_set = joblib.load('keep_q_set.pkl')
    # describe every columns and separate the classification data : define that if the set is under 10,the columns can be treated as classification
    print('数据预处理开始！')
    continue_set = [x for x in keep_q_set.keys()]
    class_set = [x for x in train_data.columns if x not in continue_set]
    continue_reshape_train_data = train_data[continue_set][:]
    # reshape the continuous data,split continuous columns into 10 sub_class
    continue_set_classed_data = continuous_data_splited(continue_reshape_train_data, keep_q_set)
    continue_set_classed_data.columns = continue_set
    cbind_classed_data_columns = continue_set + class_set
    cbind_classed_data = pd.concat(
        [train_data['uid'], continue_set_classed_data, train_data[class_set]], axis=1)
    # reshape the data to match the requirements of the trained model
    reshaped_data, daily_columns = meaningful_columns(cbind_classed_data, cbind_classed_data_columns)
    trained_columns = joblib.load('train_columns.pkl')
    reshaped_data, already_exist, not_exist = fill_data_with_trained(reshaped_data, trained_columns)
    print('预处理完成！')
    # load the trained models
    model_sklearn = joblib.load('model_sklearn.pkl')
    enc = joblib.load('enc.pkl')
    model_lr = joblib.load('model_lr.pkl')
    # train data
    correct_rank = joblib.load('correct_rank.pkl')
    print('数据加载完成！')
    y_predict = model_sklearn.predict_proba(reshaped_data[correct_rank])[:, 1]
    new_feature = model_sklearn.apply(reshaped_data[correct_rank])
    new_feature2 = np.array(enc.transform(new_feature).toarray())
    res_data = pd.DataFrame(new_feature2)
    res_data.columns = ['f' + str(x) for x in range(res_data.shape[1])]
    predict_result = model_lr.predict_proba(res_data)[:, 1]
    try:
        name_saved = str(path).replace('.txt', '') + '_output' + '.json'
        res = pd.DataFrame(predict_result)
        res.columns = ['prob']
        res.index = train_data['uid']
        res.to_json(name_saved)
    except:
        name_saved = str(path).replace('.txt', '') + '_output' + '.csv'
        pd.DataFrame(predict_result).to_csv(name_saved)
        print('uid保存失败！')
    print('预测完成，结果已保存！')


class IllegalInput(Exception):
    """
    The input data path is wrong!
    """
    pass


if __name__ == '__main__':
    main()
