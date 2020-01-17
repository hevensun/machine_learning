import pickle
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfVectorizer
import re
import jieba
import pandas as pd
import numpy as np
from pandas import Series, DataFrame
import sys
from sklearn.externals import joblib

sys.path.append('/Users/slade/Documents/YMM/Code/UCGPCG/src/jobs/terror_recognition/train_model/baseline')
from unit import metric, qieci
from train_model import _readbunchobj, readfile

file_name = '/Users/slade/Documents/YMM/Code/UCGPCG/src/jobs/terror_recognition/train_model/evaldata/evaluation_data.csv'
origin_data = pd.read_csv(open(file_name, 'rU'), header=0)
data = origin_data.iloc[:, 1:]
content = data[['content']]
content = qieci(content, 1)
origin_data['after_cut'] = content['after_cut']

with open(
        '/Users/slade/Documents/YMM/Code/UCGPCG/src/jobs/terror_recognition/train_model/new_model/model_data/vocab_emb.dat',
        'rb') as f:
    vocab_emb = pickle.load(f)

emb_train = []
label = []
dateid = []
for i in range(origin_data.shape[0]):
    line = origin_data.after_cut[i]
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
        continue
    else:
        emb_train.append(emb / cnt)
        label.append([origin_data.label[i]])
        dateid.append([origin_data.date[i]])
emb_train = np.array(emb_train)
label = np.hstack(label)
dateid = np.hstack(dateid)

mnb_tri = joblib.load(
    "/Users/slade/Documents/YMM/Code/UCGPCG/src/jobs/terror_recognition/train_model/new_model/train_model.m")

predicted_proba = mnb_tri.predict_proba(emb_train)[:, 1]

# analysis process
merge_data = pd.DataFrame(np.stack([dateid, predicted_proba, label], axis=1),
                          columns=['dateid', 'pred', 'actual'])
# eval_cv = metric(merge_data)
# merge_data['bk'] = merge_data['pred'].apply(lambda x: 1 if x > 0.01 else 0)

merge_data_15 = merge_data[merge_data.dateid == 20180915].iloc[:, 1:]
merge_data_17 = merge_data[merge_data.dateid == 20180917].iloc[:, 1:]

merge_data_15 = merge_data_15.sort_values(['pred'], ascending=False)
merge_data_17 = merge_data_17.sort_values(['pred'], ascending=False)

top_15 = merge_data_15.iloc[:117, :]
top_17 = merge_data_17.iloc[:100, :]

recall_15 = top_15[top_15.actual == 1].shape[0] / merge_data_15[merge_data_15.actual == 1].shape[0]
recall_17 = top_17[top_17.actual == 1].shape[0] / merge_data_17[merge_data_17.actual == 1].shape[0]
