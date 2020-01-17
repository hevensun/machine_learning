import pandas as pd
import numpy as np
import pickle

train_comment_path = '/Users/slade/Documents/YMM/Code/UCGPCG/src/jobs/terror_recognition/train_model/new_model/comment_cutwords.csv'
train_comment_data = pd.read_csv(open(train_comment_path, 'rU'), header=0)

train_comment_data = train_comment_data.sort_values(['label'], ascending=False)

for i in range(train_comment_data.shape[0]):
    if i == 0:
        content = train_comment_data.iloc[i, 1]
    else:
        contt = str(train_comment_data.iloc[i, 1])
        content += contt

f = open(
    '/Users/slade/Documents/YMM/Code/UCGPCG/src/jobs/terror_recognition/train_model/new_model/model_data/content.txt',
    'w')

f.write(content)
f.close()

# run sh demo.sh
# follow the bolg content

vector_path = '/Users/slade/glove/vectors.txt'
with open(vector_path, 'r') as file1:
    vocab_emb = {}
    for line in file1.readlines():
        row = line.strip().split(' ')
        vocab_emb[row[0]] = [eval(x) for x in row[1:]]

with open(
        '/Users/slade/Documents/YMM/Code/UCGPCG/src/jobs/terror_recognition/train_model/new_model/model_data/vocab_emb.dat',
        'wb') as f:
    pickle.dump(vocab_emb, f, pickle.HIGHEST_PROTOCOL)
