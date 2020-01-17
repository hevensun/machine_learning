import math
import pickle

'''
    __time__ = '2017-09-17'
    __author__ = 'sladesal'
    __blog__ = 'http://shataowei.com/2017/12/01/能够快速实现的协同推荐/'
    neighbours_number : 参考的邻居个数
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


# b1.1求出目标用户的邻居，及对应的相关程度
def neighbour(userid, user_group, item_group):
    list2user = user_group
    list2item = item_group
    neighbours = {}
    for item in list2user[userid]:
        for user in list2item[item[0]]:
            if user[0] not in neighbours.keys():
                neighbours[user[0]] = 0
            neighbours[user[0]] = neighbours[user[0]] + 1
    return neighbours


# b1.2就算用户直接的相似程度,余弦相似度
def similarity(user1, user2):
    x = 0
    y = 0
    z = 0
    for item1 in list2user[user1]:
        for item2 in list2user[user2]:
            if item1[0] == item2[0]:
                x1 = item1[1] * item1[1]
                y1 = item2[1] * item2[1]
                z1 = item1[1] * item2[1]
                x = x + x1
                y = y + y1
                z = z + z1
    if x * y == 0:
        simi = 0
    else:
        simi = z / math.sqrt(x * y)
    return simi


# 1.3计算目标用户与邻居之间的相似度：
def N_neighbour(userid, neighbours, k):
    neighbour = neighbours.keys()
    M = []
    for user in neighbour:
        simi = similarity(userid, user)
        M.append((user, simi))
    M = sorted(M, key=lambda x: x[1], reverse=True)[0:k]
    return M


# 2.列出邻居所购买过的商品并计算商品对应的推荐指数，排序得到推荐商品
def neighbour_item(matrix_value, item_num):
    M = matrix_value
    R = {}
    M1 = dict(M)
    for neighbour in M1:
        for item in list2user[neighbour]:
            if item[0] not in R.keys():
                R[item[0]] = M1[neighbour] * item[1]
            else:
                R[item[0]] = R[item[0]] + M1[neighbour] * item[1]
    Rank = sorted(R.items(), key=lambda x: x[1], reverse=True)[0:item_num]
    return Rank


if __name__ == '__main__':
    path = '/Users/slade/Documents/Yoho/personal-code/machine-learning/data/recommender/u1.base'  # 改为你的本地路径
    list2item, list2user = loaddata(path)
    user_id = 1
    neighbours_number = 3
    item_num = 10
    # 基于用户推荐
    neighbours = neighbour(user_id, list2user, list2item)
    matrix_value = N_neighbour(user_id, neighbours, neighbours_number)
    user_recommendation_result_topN = neighbour_item(matrix_value, item_num)
    # 保存数据
    output = open('user_recommendation_result_topN.pkl', 'wb')
    pickle.dump(user_recommendation_result_topN, output)
    output.close()
