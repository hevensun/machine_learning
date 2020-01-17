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
from sklearn.naive_bayes import MultinomialNB
from sklearn.externals import joblib
import sys

sys.path.append('/Users/slade/Documents/YMM/Code/UCGPCG/src/jobs/terror_recognition/train_model/baseline')
from unit import metric


'''
this is the baseline model with 3-grams
'''


def savefile(savepath, content):
    with open(savepath, "w", encoding='utf-8') as f:
        f.write(content)


def build_bounch(data, file_path):
    data_description = data.iloc[:, 1]
    data_category = data.iloc[:, 2]
    count_0 = 0
    count_1 = 0

    for a_cut, b in zip(data_description, data_category):
        if b == 0:
            savepath = file_path + '/0/' + str(count_0) + '.txt'
            try:
                savefile(savepath, a_cut)
            except:
                continue
            count_0 = count_0 + 1

        if b == 1:
            savepath = file_path + '/1/' + str(count_1) + '.txt'
            try:
                savefile(savepath, a_cut)
            except:
                continue
            count_1 = count_1 + 1


def readfile(path):
    with open(path, "rb") as f:
        content = f.read()
    return content


def corpus2Bunch(wordbag_path, destination_path):
    folder_list = [x for x in os.listdir(destination_path) if x != '.DS_Store']
    bunch = Bunch(target_name=[], label=[], filenames=[], contents=[])
    bunch.target_name.extend(folder_list)

    for folder_name in folder_list:
        detail_path = destination_path + '/' + folder_name + '/'
        file_list = os.listdir(detail_path)
        for file_name in file_list:
            full_path = detail_path + file_name
            bunch.label.append(folder_name)
            bunch.filenames.append(full_path)
            bunch.contents.append(readfile(full_path))

    with open(wordbag_path, "wb") as file_obj:
        pickle.dump(bunch, file_obj, 1)
    print("finished")


def _readbunchobj(path):
    with open(path, "rb") as file_obj:
        bunch = pickle.load(file_obj)
    return bunch


def _writebunchobj(path, bunchobj):
    with open(path, "wb") as file_obj:
        pickle.dump(bunchobj, file_obj, 1)


if __name__ == '__main__':
    train_comment_path = '/Users/slade/Documents/YMM/Code/UCGPCG/src/jobs/terror_recognition/train_model/baseline/comment_cutwords.csv'
    train_comment_data = pd.read_csv(open(train_comment_path, 'rU'), header=0)
    print(train_comment_data.head())

    # bunch_data
    bounch_path = '/Users/slade/Documents/YMM/Code/UCGPCG/src/jobs/terror_recognition/train_model/baseline/bounch_data'
    build_bounch(train_comment_data, bounch_path)
    wordbag_path = "/Users/slade/Documents/YMM/Code/UCGPCG/src/jobs/terror_recognition/train_model/baseline/model_data/bunch_set.dat"
    corpus2Bunch(wordbag_path, bounch_path)

    # tfidf/cut sequence
    stopword_path = "/Users/slade/Documents/YMM/Code/UCGPCG/src/jobs/terror_recognition/train_model/stop_words.txt"
    bunch_path = wordbag_path
    tri_space_path = '/Users/slade/Documents/YMM/Code/UCGPCG/src/jobs/terror_recognition/train_model/baseline/model_data/tri_space.dat'
    stpwrdlst = readfile(stopword_path).splitlines()

    bunch = _readbunchobj(bunch_path)
    tfidfspace = Bunch(target_name=bunch.target_name, label=bunch.label, filenames=bunch.filenames, tdm=[],
                       vocabulary={})
    vectorizer = TfidfVectorizer(stop_words=stpwrdlst, sublinear_tf=True, max_df=0.5, token_pattern=r"(?u)\b\w+\b",
                                 ngram_range=(1, 3), max_features=30000)
    tfidfspace.tdm = vectorizer.fit_transform(bunch.contents)
    tfidfspace.vocabulary = vectorizer.vocabulary_
    _writebunchobj(tri_space_path, tfidfspace)

    tri_train_set = _readbunchobj(tri_space_path)
    mnb_tri = MultinomialNB(alpha=0.001)
    mnb_tri.fit(tri_train_set.tdm, tri_train_set.label)

    f1 = mnb_tri.predict_proba(tri_train_set.tdm)[:, 1]
    actual = [int(x) for x in tri_train_set.label]

    merge_data = pd.DataFrame(np.stack([f1, actual], axis=1), columns=['pred', 'actual'])
    eval_res = metric(merge_data)
    joblib.dump(mnb_tri,
                "/Users/slade/Documents/YMM/Code/UCGPCG/src/jobs/terror_recognition/train_model/baseline/train_model.m")
