# 吴恩达视频笔记
## Gradient Checking(9-5)
```python
1.计算出你设计的梯度下降算法计算出的梯度值
2.计算(j(0+upsilon)-j(0+upsilon))/2*upsilon
双侧拆分，也存在单侧拆分，upsilon一般为1e-4，过小会产生计算问题
3.比较两者是否相似，判断梯度计算是否正确
```
## Random Initialization(9-6)
```python
随机初始化
非全0或全1的向量，否则导致前向传播的时候该节点计算出来的值都一致，影响前馈效果。
非过小或在过大的向量，否则导致反方向传播的时候的梯度要么过小要么过大，相关参数更新缓慢或者震荡。

常用：w=np.random.randn(n)/sqrt(2.0/n)
```

## Deciding What to Try Next（10-1）
```python
如何提高模型效果？
1.获取更多数据防止过拟合
2.减少特征防止过拟合
3.增加特征增强拟合能力
4.交叉特征增强拟合能力
5.正则化避免过拟合
```

## Evaluation a Hypothesis（10-3）
```python
1.考虑自由度，自由度越大模型越复杂越容易过拟合；通过改变模型的自由度来判断模型的不同自由度下模型的效果，选取最优的自由度
(在R语言里面，逐步回归就用到了这样的思想)
2.模型的效果计算，交叉检验，判断validation data效果
```

## Diagnosing Bias vs. Variance（10-4）
```python
自由度越高bias越小，var越大，过拟合的风险越大
```

## Regularization and Bias_Variance（10-5）
```python
惩罚项过大，欠拟合；惩罚项过小，过拟合

lambda选择方法，从0开始（0.01，0.02，0.04，...，10.24）共12个，交叉检验对比选择最好（我个人认为0.01开始3倍速更好，计算的次数要少很多，而且选择到最优值的可能性相差不大）
```

## Learning Curves（10-6）
```python
随着训练集合的数据量的上升，训练集的误差会上升，检验集的误差会下降，最好收敛于两个值

观察两个集合的收敛程度，判断是否有必要继续新增数据
```

## Deciding What to Do Next Revisite（10-7）
```python
如何提高模型效果？
1.获取更多数据防止过拟合（当模型存在high variance）
2.减少特征防止过拟合（当模型存在high variance）
3.增加特征增强拟合能力（当模型存在high bias ）
4.交叉特征增强拟合能力（当模型存在high bias ）
5.正则化避免过拟合（当模型存在high variance）
```

## Error Analysis（11-2）
```python
1.错分内容的高频区分规则
2.新增错分内容的高分类属性的feature
```


## Error Metrics for Skewed Classes（11-4）
```python
非平衡数据的效果体现：
recall = TP / (TP + FN)
precision = TP / (TP + FP)
F1  = 2/(1/recall+1/precision)

提高cutoff值，提升了precision，降低了recall，使得预测结果的可信性提升。
```
