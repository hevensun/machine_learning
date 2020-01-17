# Introduction
This project implement classic machine learning algorithms(ML). Motivations for this project includes:
- Helping machine learning freshman have a better and deeper understanding of the basic algorithms and models in this field.
- Providing the real-life and commercial executing methods in ML filed.
- Keeping my Mathematics Theory and Coding ability fresh due to such cases. 
- Improve my ability of Java and Python.

# Overview
### 1.FM
#### 1.1 fastfm
Show how to use the package of `fast_fm` to classify the training data directly.
#### 1.2 Fsfm
@bolg：[FM解析](http://shataowei.com/2017/12/04/FM理论解析及应用/)

We rewrite fm by ourselves and focus helping people get deeper insights about FM.So we upload it to the pypi named `Fsfm`,you can downlode it if you're interested in it.
****
### 2.N-gram
An interview problem in 'Nlp' solved by n-gram instead of Naive Bayes.
****
### 3.Svd
@bolg：[SVD解析](http://shataowei.com/2017/08/27/SVD及扩展的矩阵分解方法/)
#### 3.1 Matrix decomposition in linalg
#### 3.2 Matrix decomposition with RSVD 
****
### 4.Collaborative Filtering Recommendation System 
@bolg：[协同推荐解析](http://shataowei.com/2017/12/01/能够快速实现的协同推荐/)
#### 4.1 Base of Item
#### 4.2 Base of User
****
### 5.Semantic recognition
@bolg：[评价文本判断用户流失倾向](http://shataowei.com/2017/08/15/基于自然语言识别下的流失用户预警/)
#### 5.1 Jieba Process
#### 5.2 Tf-Idf
#### 5.3 Bp Neural Network
#### 5.4 SVM process
#### 5.5 Naive Bayes
#### 5.6 RandomForest
****
### 6.Gradient_descent
****
### 7.Smote
@bolg：[SMOTE解析](http://shataowei.com/2017/12/01/SMOTE算法/)
#### 7.1 Mean of the weight  
#### 7.2 Random scale in connected Vector
****
### 8.Frcwp
@bolg：[风控方法解析](http://shataowei.com/2017/12/09/风控用户识别方法/)

It means fast risk control with python.It's a lightweight tool that automatic recognize the outliers from a large data pool. 

****
### 9.Ensemble
@bolg:[Kaggle&TianChi分类问题相关算法快速实现
](http://shataowei.com/2017/12/28/Kaggle-TianChi分类问题相关算法快速实现/)

@bolg:[Kaggle&TianChi分类问题相关纯算法理论剖析
](http://www.shataowei.com/2017/12/28/Kaggle&TianChi分类问题相关纯算法理论剖析/)
#### 9.1 Data preprocessing before ensemble 
#### 9.2 Case showed by stacking xgboost and logistic regression
#### 9.3 Case showed by stacking gbdt and logistic regression
#### 9.4 Case showed by bagging xgboots or gbdts
#### 9.5 How to use the trained stacking model during the online module

****
### 10.Tsnewp
T-distributed stochastic neighbor embedding(t-SNE) rewrite with Python by ourselves, it's a good dimensionality reduction method.
Add many explanation among the code.

[Package download address](https://pypi.python.org/pypi?:action=display&name=Tsnewp&version=0.0.1).

[More test data](http://lvdmaaten.github.io/tsne/).

****
### 11.Knowledge Summary
Some questions for the new hand to estimate their level of the ML、DL.
What's more ,it also contains the key point which i think during my study with Andrew Ng's machine learning lessons（to be continued）.

Also, I write some words to the new hand. Read it [写给想转行机器学习深度学习的同学](http://shataowei.com/2018/03/18/写给想转行机器学习深度学习的同学/) if you're interested in it .

### 12.Youtube
Following the paper 'Deep Neural Networks for YouTube Recommendations' , finished with Python.

@bolg：[利用DNN做推荐的实现过程中的总结](https://zhuanlan.zhihu.com/p/38638747)

@bolg：[关于'Deep Neural Networks for YouTube Recommendations'的一些思考和实现](http://www.shataowei.com/2018/06/26/关于Deep-Neural-Networks-for-YouTube-Recommendations的一些思考和实现/)

****

### 13.FFM
See More From:

@bolg：[基于Tensorflow实现FFM](http://shataowei.com/2018/08/06/基于Tensorflow实现FFM/)

More you may follow with interest ：**[FM部分](https://github.com/sladesha/machine_learning/tree/master/FM)**||**[deepFM部分](https://github.com/sladesha/deep_learning/tree/master/DeepFM)**

****

### 14.GolVe_Classification
See More From:

@bolg：[GolVe向量化做文本分类](http://www.shataowei.com/2018/09/25/GloVe向量化做文本分类/)

More you may follow with interest ：**[Youtube构造skn Vector](http://www.shataowei.com/2018/06/26/关于Deep-Neural-Networks-for-YouTube-Recommendations的一些思考和实现/)**||**[N-Grams](https://github.com/sladesha/machine_learning/tree/master/n-gram)**

****

### 15.YMMNlpUtils
- Phone number analytical tools, design for get out the true phone number from digital mixed with dialect、chinese、special symbols
- Adjust that is any phone communication intention inside the conversation, base model coming from the result translated by IFLYTEK

`pip install YMMNlpUtils==0.1.1`  supported

download directly supported, here's the url: [YMMNlpUtils 0.1.1](https://pypi.org/project/YMMNlpUtils/0.1.1/)

- [DEMO1](http://www.shataowei.com/2019/05/13/中文语境下的手机号识别/)
- [DEMO2](http://www.shataowei.com/2019/06/25/语音转译后是否文本意图识别-YMMNlpUtils/)

****

### 16.Neologism

- 已知词扩展
    - text_base = Neologism(st=text, prev_cut=True, macth_posseg=\[\["a"], \["n"]])
    - text_base.filter(frequency=0.001, freedom=0.5)
- 新词发现    
    - direct_search = Neologism(st=text, prev_cut=False)
    - direct_search.filter(frequency=0.0001, polymerization=15, freedom=0.5))
    
### 17.Bayes_Optimizaion

@bolg：[Bayes_Optimizaion based on GP + UCB](http://www.shataowei.com/2019/12/07/Auto-Machine-Learning初探/)

### 18.TFIDF

- Java实现，Main为调用方式测试
- NLP文本重要性计算

### 19.SimiHash

- NLP文本去重 
- SimiHash为Java实现
	- Main为调用方式测试
- WordClassificationDeduplication为python版本
	- Main为调用方式测试

### 20.BM25

- Java实现，Main为调用方式测试
- NLP文本重要性计算
- 关键词提取

### 21.TextRank

- TextRankSummary用来做摘要提取，衍生自PageRank的迭代思想
- TextRankKeyWord用来做关键词提取，衍生自PageRank的迭代思想

### 22.Rake

- 关键词抽取，衍生自频率（freq）+由共现度得到的度（deg）的思想，score = deg/freq，论文：[Automatic Keyword Extraction from Individual Documents](https://www.researchgate.net/publication/227988510_Automatic_Keyword_Extraction_from_Individual_Documents)
- 优点：
    - 快，算法简单而高效
    - 能够提取一些较长的专业术语
- 缺点：
    - 可以做召回，但是精确度欠佳
    - 原论文基于英文，可切分词比较多，中文无法找到类似and ，or 这种切分词进行分段
- 实现：
    - 平衡了高频词对全文的影响
    - 采取了有效词长平衡，避免长文本造成的数据有偏现象
- 版本：
    - 支持Java版本，依赖HanNlp分词器
    - 支持Python版本，依赖jieba分词器


# Requirements
Python Environment.
More details getting from single project requirement.

# More
If you find some incorrect content, i'm so sorry about that. PLS contact me by the following way:
- WeChat:sharalion
- E-mail:stw386@sina.com
- Message Board in my [bolg](http://shataowei.com)
