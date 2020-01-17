from  operator import *
from functools import reduce
import math
import pickle
import os

def load_data(path):
    f = open(path)
    words = []
    for info in f.readlines():
        word_list = info.strip().split(' ')
        if len(word_list) > 0:
            for i in word_list:
                word_single = i.replace('.', '')
                word_single = word_single.replace('?', '')
                word_single = word_single.replace('!', '')
                word_single = word_single.replace('"', '')
                word_single = word_single.replace('\'s', '')
                word_single = word_single.replace(',', '')
                word_single = word_single.replace('_', '')
                word_single = word_single.replace(';', '')
                word_single = word_single.replace('-', '')
                word_single = word_single.replace('=', '')
                word_single = word_single.replace(')', '')
                word_single = word_single.replace('(', '')
                if word_single.isalpha():
                    words.append(word_single.lower())
    return words


# 构造语料库
def make_corpus(words):
    corpus = dict()
    for word in set(words):
        corpus[word] = words.count(word)
    return corpus


# 统计单字母和双字母和三字母的出现次数
def frequency(symbol, corpus):
    l = len(symbol)
    freq = 0
    for word in corpus.keys():
        freq_i = 0
        for i in range(len(word)):
            if l == 1:
                if word[i] == symbol:
                    freq_i += 1
            if l == 2:
                if word[i:i + 2] == symbol:
                    freq_i += 1
            if l == 3:
                if word[i:i + 3] == symbol:
                    freq_i += 1
        freq_i = freq_i * corpus[word]
        freq += freq_i
    return freq


# 条件概率
# 平滑算法：(aimed_word_num+1)/(condition_word_num+all_word_number)
# 平滑算法2：(aimed_word_num+1)/(set(condition_word_num)+2)
def condition_prob(w1, w2, corpus):
    freq_w1 = frequency(w1, corpus)
    freq_w2 = frequency(w2, corpus)
    return (float(freq_w2) + 1) / (float(freq_w1) + len(corpus.keys()))


# n-gram部分：
def ngram(word, corpus):
    # 首项
    cond_probs = []
    cond_p = (frequency(word[0], corpus) + 1) / (2 * len(corpus.keys()))
    cond_probs.append(cond_p)
    # 次首项
    cond_p = condition_prob(word[0], word[0:2], corpus)
    cond_probs.append(cond_p)
    # 中间项
    for i in range(len(word) - 2):
        cond_p = condition_prob(word[i:i+2], word[i:i + 3], corpus)
        cond_probs.append(cond_p)
    # 次尾项
    cond_p = condition_prob(word[-1], word[-2:], corpus)
    cond_probs.append(cond_p)
    # 尾项
    cond_p = (len(corpus.keys()) + 1) / (frequency(word[-1], corpus) + len(corpus.keys()))
    cond_probs.append(cond_p)

    prob = reduce(mul, cond_probs) * math.pow(10, len(word))
    return prob


if __name__ == '__main__':
    path = '/Users/slade/Documents/Yoho/personal-code/machine-learning/data/eng.txt'
    # load data
    words = load_data(path)
    if os.path.exists('/Users/slade/corpus.pkl'):
        pkl_file = open('/Users/slade/corpus.pkl', 'rb')
        corpus = pickle.load(pkl_file)
    else:
        corpus = make_corpus('corpus.txt')
    word_probility = dict()
    for i in set(corpus.keys()):
        probility = ngram(str(i), corpus)
        word_probility[i] = probility
        print('the word:%s is %f' %(i,probility))
    if os.path.exists('/Users/slade/word_probility.pkl'):
        pass
    else:
        output = open('word_probility.pkl', 'wb')
        pickle.dump(word_probility, output)
        output.close()

    # output = open('corpus.pkl', 'wb')
    # pickle.dump(corpus, output)
    # output.close()
    #
    # pkl_file = open('corpus.pkl', 'rb')
    # corpus = pickle.load(pkl_file)
