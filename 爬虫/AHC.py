# -*- coding: utf-8 -*-
"""
Created on Mon May 27 16:02:22 2019

@author: Stella
"""
import math
import numpy
import time
import sys
#import hierarchicalClustering
#import untitled0
from matplotlib import pyplot as plt
##f, companies, dates = hierarchicalClustering.main()
#f, companies, dates = untitled0.main()
#print(f)
#r = open(r'results/industries/results.txt','a')
#sys.stdout = r
#sys.stderr = r 
def print_matrix(matrix):
    print("[matrix] width : %d height : %d" % (len(matrix[0]), len(matrix)))
    for i in range(len(matrix)):
        print(matrix[i])
# always put the diagonal element as our first choice
def min_abc_index(a,b,c):
    if(b < c):
        if(a < b):
            return -1, 0
        else:
            return 0, -1
    elif (a < c):
            return -1, 0
    return -1, -1
def min_abc(a,b,c):
    min_abc = c
    if(b < c):
        min_abc = b
        if(a < b):
            min_abc = a
    elif (a < c):
            min_abc = a
    return min_abc
# Euclidean Distance of dataframe
def euclidean_dist(f, a, b):  
    return math.sqrt(f.apply(lambda x: (x[a] - x[b])**2, axis=1).sum())
def e_dist(a,b):
     return numpy.sqrt(numpy.sum(numpy.square(numpy.array(a) - numpy.array(b))))
# norm of vector (as distance) equals with euclidean
def n_dist(a,b):
    return numpy.linalg.norm((numpy.array(a) - numpy.array(b)))
# DTW distance
def dtw_dist(c, d):
    a = numpy.array(c)
    b = numpy.array(d)
    dist_matrix = [([0 for j in range(len(a)+1)]) for i in range(len(b)+1)]
    for i in range(1, len(a)+1):
        for j in range(1, len(b)+1):
            dist_matrix[j][i] = abs(a[i-1] - b[j-1])
    # acumulate distance
    for i in range(1, len(a)+1):
        for j in range(1, len(b)+1):
            dist_matrix[j][i] += min_abc(dist_matrix[j-1][i], dist_matrix[j][i-1], dist_matrix[j-1][i-1])
#    print_matrix(dist_matrix)
# store the best alignment path and similirity
    i = len(a); j = len(b)
    path = [(j,i)]
    W = []
    W.append(dist_matrix[j][i])
    while (i !=0 and j != 0):
        x, y = min_abc_index(dist_matrix[j-1][i], dist_matrix[j][i-1], dist_matrix[j-1][i-1])
        j += x; i += y
        if (j == 0 and i != 0):
            j += 1
        if (i == 0 and j != 0):
            i += 1
        W.append(dist_matrix[j][i])      
        path.append((j,i))
#    print(path)
    return (numpy.sum(W)/(len(path)-1))    
def complete_linkage(Ci, Cj, dist, f):
    if (dist == euclidean_dist):
        return max(dist(i, j) for i in Ci for j in Cj)
    else:
        return max(dist(f[i],f[j]) for i in Ci for j in Cj)  
def single_linkage(Ci, Cj, dist, f):
    if (dist == euclidean_dist):
        return min(dist(i, j) for i in Ci for j in Cj)
    else: 
        return min(dist(f[i],f[j]) for i in Ci for j in Cj)
def average_linkage(Ci, Cj, dist, f):
    if (dist == euclidean_dist):
        return sum(dist(i, j) for i in Ci for j in Cj)/(len(Ci)*len(Cj))
    return sum(dist(f[i], f[j]) for i in Ci for j in Cj)/(len(Ci)*len(Cj))
# find the companis (index) that have minimum distance
def find_Min(M):
    minSet = 3000
    x = 0; y = 0
    for i in range(len(M)):
        for j in range(len(M[i])):
            if i != j and M[i][j] < minSet:
                minSet = M[i][j]
                x = i
                y = j
    return (x, y, minSet)    
# the main part of AHC algorithm, k 是最终聚类的簇数
def AHC(f, k, dates):
    # C stores all clusters 
    C = []
    for i in f:
        Ci = []
        Ci.append(i)
        C.append(Ci)        
    print("total companies list: ", C)
    # M stores distance 计算每个原始数据两两的欧式距离
    M = []
    for i in f:
        Mi = []
#        print(f[i]) # f[i] is each colume of dataframe with Name
        for j in f:
#            Mi.append(euclidean_dist(f, i, j))
            Mi.append(n_dist(f[i], f[j]))
        M.append(Mi)
    n_clusters = len(C) 
    print("original clusters: ", n_clusters)
    while (n_clusters > k):
        # find clusters that have minimum distance and combine them
        x, y, minS = find_Min(M)
        C[x].extend(C[y])
        C.remove(C[y])     
        M = []
        # calculate dissimilirity/distance using linkage
        for i in C:
            Mi = []
            for j in C:
                Mi.append(average_linkage(i, j, dtw_dist, f))
            M.append(Mi)     
        n_clusters -= 1
        if (n_clusters < 5):
           for i in C:
               plt.figure(dpi=128, figsize=(12, 5))
               for j in i: 
                   plt.plot(dates, f[j], label = j)
           plt.legend()
           plt.savefig('results/20_ACH/'+ str(len(C)) + '_' +'.png')
           plt.show()
#tic = time.clock()
#AGNES(f, single_linkage, euclidean_dist, z)
#toc = time.clock()
#print("dist.euclidean: %.3fs " % (toc - tic))

#tic = time.clock()
#AGNES(f, single_linkage, n_dist, z)
#toc = time.clock()
#print("np.linalg.norm & single_linkage: %.3fs" % (toc - tic))
#
#
##AGNES(f, single_linkage, dtw_dist, z)
#tic = time.clock()
#AGNES(f, complete_linkage, n_dist, z)
#toc = time.clock()
#print("np.linalg.norm & complete_linkage: %.3fs" % (toc - tic))
#tic = time.clock()
#AHC(f, average_linkage, n_dist, z)
#toc = time.clock()
#print("np.linalg.norm & average_linkage: %.3fs" % (toc - tic))
#

#r.close()