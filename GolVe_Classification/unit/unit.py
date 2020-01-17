import pandas as pd
import re
import jieba


def metric(data):
    print('first columns should be predict ones')
    black_recall = []
    white_precision = []
    cof = []
    Negative_ones = []
    for i in range(1, 100):
        update_df = data.copy()
        cutoff = i / 100
        update_df.columns = ['p', 'a']
        update_df['mapres'] = update_df['p'].apply(lambda x: 1 if x > cutoff else 0)
        black_recall.append(
            update_df[update_df.a == 1][update_df.mapres == 1].shape[0] / update_df[update_df.a == 1].shape[0])
        white_precision.append(
            update_df[update_df.mapres == 0][update_df.a == 0].shape[0] / update_df[update_df.mapres == 0].shape[0])
        cof.append(i / 100)
        Negative_ones.append(update_df[update_df.mapres == 1].shape[0] / update_df.shape[0])
    return black_recall, white_precision, cof, Negative_ones


def qieci(data, palce=2):
    cut_word = []
    # 新增**的敏感词段
    rule = re.compile("[^\u4e00-\u9fa5a-z0-9*]")
    # 更改词库
    jieba.load_userdict('/Users/slade/Documents/YMM/Code/UCGPCG/src/jobs/terror_recognition/train_model/dict.txt')
    data_description = data.iloc[:, 0]
    for a in data_description:
        a = rule.sub("", a.lower())
        a_cut = jieba.cut(a)
        a_cut = ' '.join(a_cut)
        cut_word.append(a_cut)
    data.insert(palce, 'after_cut', cut_word)
    return data

