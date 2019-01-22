#!/usr/bin/env python
# -*- coding=utf-8 -*-
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

import cv2
import numpy as np
from math import *
import os
import time
def cossimilar(x, y):
    x = np.array(x, dtype='float32')
    y = np.array(y, dtype='float32')
    res = (x.dot(y.T)) / (np.linalg.norm(x) * np.linalg.norm(y))
    res = 0.5 + res * 0.5
    return res
def touying(p, HASH):
    p = lianghua(p, 0.345166, 0.319847)
    touying = subtoham(p, HASH)
    return touying
def Vector(img):
    B= cv2.split(img)[0]
    G= cv2.split(img)[1]
    R= cv2.split(img)[2]
    height= img.shape[0]
    width = img.shape[1]
    b1 = B[0:int(height / 2), 0:int(width / 2)].sum()
    g1 = G[0:int(height / 2), 0:int(width / 2)].sum()
    r1 = R[0:int(height / 2), 0:int(width / 2)].sum()
    total1 = b1 + g1 + r1
    b2 = B[0:int(height / 2), int(width / 2) + 1:width].sum()
    g2 = G[0:int(height / 2), int(width / 2) + 1:width].sum()
    r2 = R[0:int(height / 2), int(width / 2) + 1:width].sum()
    total2 = b2 + g2 + r2
    b3 = B[0:int(height / 2)+ 1, int(width / 2):width].sum()
    g3 = G[0:int(height / 2)+ 1, int(width / 2):width].sum()
    r3 = R[0:int(height / 2)+ 1, int(width / 2):width].sum()
    total3 = b3 + g3 + r3
    b4 = B[0:int(height / 2)+ 1, int(width / 2) + 1:width].sum()
    g4 = G[0:int(height / 2)+ 1, int(width / 2) + 1:width].sum()
    r4 = R[0:int(height / 2)+ 1, int(width / 2) + 1:width].sum()
    total4 = b4 + g4 + r4
    b1=float(b1) / total1
    b2=float(b2) / total2
    b3=float(b3) / total3
    b4=float(b4) / total4
    g1=float(g1) / total1
    g2=float(g2) / total2
    g3=float(g3) / total3
    g4=float(g4) / total4
    r1=float(r1) / total1
    r2=float(r2) / total2
    r3=float(r3) / total3
    r4=float(r4) / total4
    vector=[b1,g1,r1,b2,g2,r2,b3,g3,r3,b4,g4,r4]
    return vector
def lianghua(p, high, low):
    q = [0] * len(p)
    for i in range(len(p)):
        if p[i] > high:
            q[i] = 2
        elif p[i] > low:
            q[i] = 1
        else:
            q[i] = 0
    return q
def subtoham(p, cast_set):
    result = ""
    for num in cast_set:
        xi = int(round(float(num) / 2.0) - 1)
        if (p[xi] == 0):
            result += "0"
        elif (p[xi] == 2):
            result += "1"
        else:
            result += str((num - 2 * xi) % 2)
    return result
def LSH(urls):
    filename="target3.jpg"
    filepath="img"
    castset = [1, 3,5, 7, 8,12,22]
    buckets = {}
    files = os.listdir(filepath)
    for file in files:
        pic = cv2.imread(filepath + "/" + file, cv2.IMREAD_COLOR)
        vec = Vector(pic)
        p = touying(vec, castset)
        if (buckets.has_key(p)):
            buckets[p].append([file, vec])
        else:
            buckets[p] = [[file, vec]]

    start = time.time()
    target = cv2.imread(urls, cv2.IMREAD_COLOR)
    targetvec = Vector(target)
    targetp = touying(targetvec, castset)

    if (not buckets.has_key(targetp)):
        print "NO RESULT"
        return
    else:
        print "Filename\tSimilarity"

        allsimilarity = []
        for ele in buckets[targetp]:
            allsimilarity.append((ele[0], cossimilar(targetvec, ele[1])))
        allsimilarity.sort(key=lambda x: x[1], reverse=True)
        results=[]
        for i in range(min(len(allsimilarity),10)):
            print allsimilarity[i][0], "\t\t", allsimilarity[i][1]
            results.append(allsimilarity[i][0])
        return results
def NN():
    filename = "target3.jpg"
    filepath = "img"
    start = time.time()
    target = cv2.imread(filename, cv2.IMREAD_COLOR)
    targetvec = Vector(target)
    allsimilarity = []
    files= os.listdir(filepath)
    for file in files:
        pic = cv2.imread(filepath + "/" + file, cv2.IMREAD_COLOR)
        vec = Vector(pic)
        allsimilarity.append((file, cossimilar(vec, targetvec)))
    allsimilarity.sort(key=lambda x: x[1], reverse=True)
    print "Filename\tSimilarity"

    for i in range(4):
        print allsimilarity[i][0], "\t\t", allsimilarity[i][1]
    print "cost", time.time() - start, "s"

LSH()
