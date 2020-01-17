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
data['after_cut'] = content['after_cut']

stopword_path = "/Users/slade/Documents/YMM/Code/UCGPCG/src/jobs/terror_recognition/train_model/stop_words.txt"
tri_space_path = '/Users/slade/Documents/YMM/Code/UCGPCG/src/jobs/terror_recognition/train_model/baseline/model_data/tri_space.dat'
train_set = _readbunchobj(tri_space_path)

stpwrdlst = readfile(stopword_path).splitlines()

vectorizer = TfidfVectorizer(sublinear_tf=True, max_df=0.5, vocabulary=train_set.vocabulary)
tdm = vectorizer.fit_transform(data["after_cut"])

mnb_tri = joblib.load(
    "/Users/slade/Documents/YMM/Code/UCGPCG/src/jobs/terror_recognition/train_model/baseline/train_model.m")
predicted_proba = mnb_tri.predict_proba(tdm)[:, 1]

# analysis process
merge_data = pd.DataFrame(np.stack([origin_data['date'], predicted_proba, data['label']], axis=1),
                          columns=['dateid', 'pred', 'actual'])
eval_cv = metric(merge_data)
merge_data['bk'] = merge_data['pred'].apply(lambda x: 1 if x > 0.01 else 0)

merge_data_15 = merge_data[merge_data.dateid == 20180915].iloc[:, 1:]
merge_data_17 = merge_data[merge_data.dateid == 20180917].iloc[:, 1:]

merge_data_15 = merge_data_15.sort_values(['pred'], ascending=False)
merge_data_17 = merge_data_17.sort_values(['pred'], ascending=False)

top_15 = merge_data_15.iloc[:117, :]
top_17 = merge_data_17.iloc[:100, :]

recall_15 = top_15[top_15.actual == 1].shape[0] / merge_data_15[merge_data_15.actual == 1].shape[0]
recall_17 = top_17[top_17.actual == 1].shape[0] / merge_data_17[merge_data_17.actual == 1].shape[0]
