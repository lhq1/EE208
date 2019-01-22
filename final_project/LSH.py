import cv2
# -- coding: utf-8 --
import cv2
import numpy as np
import os
import time

def pre_count():
    lis = []
    for i in os.listdir('img'):
        file = 'img/' + i
        lis.extend(merge_vector(file))
    lis.sort()
    l1 = 4 * len(os.listdir('img'))
    l2 = 8 * len(os.listdir('img'))
    print(lis[l1])
    print(lis[l2])


def map(m):
    if 0 <= m < 0.32:
        return 0
    elif 0.32 <= m <= 0.35:
        return 1
    else:
        return 2


def vector(img, h1, h2, w1, w2):
    channels = cv2.split(img[h1:h2,w1:w2])
    lis = []
    sum = 0
    for i in channels:
        lis.append(i.sum())
        sum += i.sum()
    for i in range(3):
        lis[i] = map(lis[i]/sum)
        #lis[i] = lis[i] / sum
    return lis


def merge_vector(file):
    img = cv2.imread(file)
    h,w = img.shape[0],img.shape[1]
    mh = int(h/2) # medium height
    mw = int(w/2) # medium width
    res = []
    res.extend(vector(img,0,mh,0,mw))
    res.extend(vector(img,0,mh, mw, w))
    res.extend(vector(img, mh, h, 0, mw))
    res.extend(vector(img, mh, h, mw, w))
    return res


def hash(vector, map_set):
    I = [[] for x in range(12)]
    lsh = []
    for i in map_set:
       I[(i-1)//2].append(i)
    for i in range(12):
        if len(I[i]) == 0:
            continue
        for j in I[i]:
            lsh.append(0+(j-2*i <= vector[i]))
    return lsh


def process_set(dir,map_set):
    res = []
    for i in os.listdir(dir):
        file = dir + '/'+i
        vector = merge_vector(file)
        arr = np.array(hash(vector,map_set))
        arr = arr / np.linalg.norm(arr)
        res.append([arr, file])
    return res


# 比较得到相似度最大的图片名称，如果多个图片相似度均等于最大相似度，将它们全部返回
def get_max(lis):
    max = 0
    good = []
    for i in range(len(lis)):
        if lis[i][0] > max:
            max = lis[i][0]
    for i in range(len(lis)):
        if lis[i][0] == max:
            good.append(lis[i][1])
    return good


def LSH_algorithm():
    t1 = time.time()
    search_vec = merge_vector('target.jpg')
    map_set = [13,14, 15,17,18,19,20,21]
    search_lsh = np.array(hash(search_vec, map_set))
    search_lsh = search_lsh / np.linalg.norm(search_lsh)
    res = process_set('img',map_set)
    lis = []
    for item, name in res:
        lis.append([np.dot(item, search_lsh), name])
    t2 = time.time()
    print('result of LSH:',get_max(lis))
    print('time of LSH:', t2 - t1)


def NN_algorithm():
    t1 = time.time()
    vec1 = np.array(merge_vector('target.jpg'))
    vec1 = vec1 / np.linalg.norm(vec1)
    lis = []
    for i in os.listdir('img'):
        file = 'img/' + i
        vec2 = np.array(merge_vector(file))
        vec2 = vec2 / np.linalg.norm(vec2)
        lis.append([np.dot(vec1,vec2),file])
    t2 = time.time()
    print('result of NN:',get_max(lis))
    print('time of NN:',t2 - t1)


LSH_algorithm()
NN_algorithm()
