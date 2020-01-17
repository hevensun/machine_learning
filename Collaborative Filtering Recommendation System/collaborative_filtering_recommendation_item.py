from collections import defaultdict
import math
import pickle

'''
    __time__ = '2017-09-17'
    __author__ = 'sladesal'
    __blog__ = 'http://shataowei.com/2017/12/01/能够快速实现的协同推荐/'
    item_num ： 想要推荐的商品个数
'''


def loaddata(location):
    list2item = {}  # 商品对应的用户列表
    list2user = {}  # 用户对应的商品列表
    f = open(location, 'r')
    data = f.readlines()
    data = [x.split('\t') for x in data]
    f.close()

    for i in data:
        if int(i[1]) not in list2item.keys():
            list2item[int(i[1])] = [[int(i[0]), int(i[2])]]
        else:
            list2item[int(i[1])].append([int(i[0]), int(i[2])])

        if int(i[0]) not in list2user.keys():
            list2user[int(i[0])] = [[int(i[1]), int(i[2])]]
        else:
            list2user[int(i[0])].append([int(i[1]), int(i[2])])
    return list2item, list2user


# a1.1统计各商品出现次数
def itemcf_itemall(userlist):
    I = {}
    for key in userlist:
        for item in userlist[key]:
            if item[0] not in I.keys():
                I[item[0]] = 0
            I[item[0]] = I[item[0]] + 1
            # 1.2计算相似矩阵
    C = defaultdict(defaultdict)
    W = defaultdict(defaultdict)
    # 根据用户的已购商品来形成对应相似度矩阵
    for key in userlist:
        for item1 in userlist[key]:
            for item2 in userlist[key]:
                if item1[0] == item2[0]:
                    continue
                if item2[0] not in C[item1[0]].keys():
                    C[item1[0]][item2[0]] = 0
                C[item1[0]][item2[0]] = C[item1[0]][item2[0]] + 1
                # 计算相似度，并填充上面对应的相似度矩阵
    for i, j in C.items():
        for z, k in j.items():
            W[i][z] = k / math.sqrt(I[i] * I[z])
    return I, W


# a2.寻找用户观看的其他item
def item_recommendation(similarity_matrix, userid, item_num):
    W = similarity_matrix
    score_final = defaultdict(int)
    useriditem = []
    for item, score in list2user[userid]:
        # 3.计算用户的item得分，k来控制用多少个相似商品来计算最后的推荐商品
        for i, smimilarity in sorted(W[item].items(), key=lambda x: x[1], reverse=True)[0:item_num]:
            for j in list2user[userid]:
                useriditem.append(j[0])
            if i not in useriditem:
                score_final[i] = score_final[i] + smimilarity * score
                # 最后的10控制输出多少个推荐商品
    l = sorted(score_final.items(), key=lambda x: x[1], reverse=True)[0:10]
    return l


if __name__ == '__main__':
    path = '/Users/slade/Documents/Yoho/personal-code/machine-learning/data/recommender/u1.base'  # 改为你的本地路径
    list2item, list2user = loaddata(path)
    item_times, item_mat = itemcf_itemall(list2user)
    # 基于商品推荐
    user_id = 1
    item_num = 10
    user_recommendation_result_topN = item_recommendation(item_mat, user_id, item_num)
    # 保存数据
    output = open('user_recommendation_result_topN.pkl', 'wb')
    pickle.dump(user_recommendation_result_topN, output)
    output.close()
