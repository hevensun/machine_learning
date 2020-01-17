import pandas as pd
import numpy as np
from sklearn.datasets.base import Bunch
import os
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cross_validation import train_test_split
import random
from collections import defaultdict
from sklearn.linear_model import LogisticRegressionCV, LinearRegression
from sklearn.metrics import roc_auc_score
from snownlp import SnowNLP
from sklearn.externals import joblib
import sys

sys.path.append('/Users/slade/Documents/YMM/Code/UCGPCG/src/jobs/terror_recognition/train_model/baseline')
from unit import metric, qieci

if __name__ == '__main__':
    # load data
    train_comment_path = '/Users/slade/Documents/YMM/Code/UCGPCG/src/jobs/terror_recognition/train_model/new_model/comment_cutwords.csv'
    train_comment_data = pd.read_csv(open(train_comment_path, 'rU'), header=0)
    print(train_comment_data.head())

    with open(
            '/Users/slade/Documents/YMM/Code/UCGPCG/src/jobs/terror_recognition/train_model/new_model/model_data/vocab_emb.dat',
            'rb') as f:
        vocab_emb = pickle.load(f)

    emb_train = []
    label = []
    for i in range(train_comment_data.shape[0]):
        line = train_comment_data.after_cut[i]
        cnt = 0
        try:
            seq = line.split(' ')
        except:
            print('not a common sequence')
            print(line)
            continue
        for word in seq:
            try:
                if cnt == 0:
                    emb = np.array(vocab_emb[word])
                else:
                    emb += np.array(vocab_emb[word])
                cnt += 1
            except:
                continue
        if np.isnan(sum(emb / cnt)):
            print('not a common length')
            print(line)
        else:
            emb_train.append(emb / cnt)
            label.append([train_comment_data.label[i]])
    emb_train = np.array(emb_train)
    label = np.hstack(label)

    lr = LogisticRegressionCV(multi_class="ovr", fit_intercept=True, Cs=np.logspace(-2, 2, 20), cv=2, penalty="l2",
                              solver="lbfgs", tol=0.01, class_weight={0: 0.1, 1: 0.9})
    re = lr.fit(emb_train, label)

    f1 = lr.predict_proba(emb_train)[:, 1]
    merge_data = pd.DataFrame(np.stack([f1, label], axis=1), columns=['pred', 'actual'])
    eval_res = metric(merge_data)
    joblib.dump(re,
                "/Users/slade/Documents/YMM/Code/UCGPCG/src/jobs/terror_recognition/train_model/new_model/train_model.m")
