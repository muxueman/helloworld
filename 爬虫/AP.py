# -*- coding: utf-8 -*-
"""
Created on Sat Jun  1 12:19:46 2019

@author: Stella
"""
from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
from datetime import datetime
import os
import csv
from sklearn.covariance import GraphLassoCV
from sklearn.cluster import AffinityPropagation
import AHC



def verse(list):
    verse_list = []
    for ele in reversed(list):
        verse_list.append(ele)
    return verse_list
# 这里输出的是一个股票的所有数据 dataframe格式
def read_csv(csv_file):
    f = pd.DataFrame()
    dates, closes, opens, highs, lows, changes= [], [], [], [], [], []
    end_date = datetime.strptime("2019/4/10",'%Y/%m/%d')
    start_date = datetime.strptime("2019/2/21",'%Y/%m/%d')
    # 使用csv.reader读取csvfile中的文件
    with open(csv_file, encoding="utf-8") as csvfile:
        csv_reader = csv.reader(csvfile)  
        stock_header = next(csv_reader) 
        for row in csv_reader: 
            # 数据格式化
            date = datetime.strptime(row[0], '%b %d, %Y')
            if (start_date < date and date < end_date):
                dates.append(date)
                closes.append(float(row[1].replace(",", "")))
                opens.append(float(row[2].replace(",", "")))
                highs.append(float(row[3].replace(",", "")))
                lows.append(float(row[4].replace(",", "")))
                changes.append(float(row[6].replace("%", "")))
    f['dates'] = verse(dates)
    f['closes'] = verse(closes)
    f['opens'] = verse(opens)
    f['highs'] = verse(highs)
    f['lows'] = verse(lows)
    f['changes'] = verse(changes)
    return f, verse(changes)

# 这里读取每一个文件 把股票的某个特征提取出来 不同的股票整合为不同的列 列名是股票名
def read_all_data(files):
    i = 0 # i 限制读取的个数
    df_dataset = pd.DataFrame()
    companies = []
    dataset = []
    for file in files:
        i += 1
        csv_path = 'database/'+file
        f, data_change = read_csv(csv_path)
        label = file.split(" ")[0]
        companies.append(label)
        #检测数据的一致性 显示不符合的数据删掉
#        print(len(f['dates']))
        if (len(f['dates']) != 33):
            print(file, "not qualify!") 
        else:
            if (-1 < i and i < 21):
                # 这里可以选取不同的参数
                df_dataset[label] = f['changes'] 
                dataset.append(data_change)
                dates = f['dates']
    # dataset 是数组， df-feature 是datafram格式
    return dataset, df_dataset, companies, dates

def AP(a):
    ap = AffinityPropagation(preference=-50).fit(a)
    cluster_centers_indices = ap.cluster_centers_indices_    # 预测出的中心点的索引，如[123,23,34]
    labels = ap.labels_    # 预测出的每个数据的类别标签,labels是一个NumPy数组
    print(labels)
    n_clusters_ = len(cluster_centers_indices)
    print('预测的聚类中心个数：%d' % n_clusters_)
    for p in range(0, n_clusters_):
        plt.figure(dpi=128, figsize=(12, 7))
        for i in range(0, len(labels)):
            t = 0
            if (labels[i] == p):
                t += 1                
                plt.plot(dates, a[i], label = companies[i]) 
        plt.legend()
        plt.grid(ls='--')
        plt.title(p)
#        plt.savefig('results/20_AP/'+ str(p) +'.png')
        plt.show()  
    #print('同质性：%0.3f' % metrics.homogeneity_score(labels_true, labels))
    #print('完整性：%0.3f' % metrics.completeness_score(labels_true, labels))
    #print('V-值： % 0.3f' s% metrics.v_measure_score(labels_true, labels))
    #print('调整后的兰德指数：%0.3f' % metrics.adjusted_rand_score(labels_true, labels))
    #print('调整后的互信息： %0.3f' % metrics.adjusted_mutual_info_score(labels_true, labels))
    #print('轮廓系数：%0.3f' % metrics.silhouette_score(X, labels, metric='sqeuclidean'))

    

dirs = os.listdir('database/')  
print("the length of total companies: ",len(dirs))
dataset, df_dataset, companies, dates = read_all_data(dirs)
print("the length of dates to ", dates[0], ": ", len(dates))
#print(dataset)  # 对AP算法用
#print(df_dataset)  # 对AHC算法用
AHC.AHC(df_dataset, 3, dates)
#AP(dataset)

# 将股票数据DataFrame转变为np.ndarray
stock_dataset=np.array(dataset).astype(np.float64)
#print(dataset)
#print(a)


 

## 绘制图表展示
#from itertools import cycle
#
#colors = cycle('bgrcmykbgrcmykbgrcmykbgrcmyk')
## 循环为每个类标记不同的颜色
#for k, col in zip(range(n_clusters_), colors):
#    # labels == k 使用k与labels数组中的每个值进行比较
#    # 如labels = [1,0],k=0,则‘labels==k’的结果为[False, True]
#    class_members = labels == k
#    cluster_center = a[cluster_centers_indices[k]]    # 聚类中心的坐标
#    plt.plot(a[class_members, 0], a[class_members, 1], col + '.')
#    plt.plot(cluster_center[0], cluster_center[1], markerfacecolor=col,
#             markeredgecolor='k', markersize=14)
#    for x in a[class_members]:
#        plt.plot([cluster_center[0], x[0]], [cluster_center[1], x[1]], col)
#
#plt.title('预测聚类中心个数：%d' % n_clusters_)
#plt.show()
#
#
#
#
#
#
#
#
#
#
#
#

## 从相关性中学习其图形结构
#edge_model=GraphLassoCV()
#edge_model.fit(stock_dataset)
#
#
#
#
#
#
## 使用近邻传播算法构建模型，并训练LassoCV graph
#
#X,ls=affinity_propagation(edge_model.covariance_)
#
##
#print(ls)
#print('Stock Clusters: {}'.format(n_labels+1)) # 10，即得到10个类别
#sz50_df2=sz50_df.set_index('code')
# print(sz50_df2)
#for i in range(n_labels+1):
#    # print('Cluster: {}----> stocks: {}'.format(i,','.join(np.array(selected_stocks)[labels==i]))) # 这个只有股票代码而不是股票名称
#    # 下面打印出股票名称，便于观察
#    stocks=np.array(selected_stocks)[labels==i].tolist()
#    names=sz50_df2.loc[stocks,:].name.tolist()
#    print('Cluster: {}----> stocks: {}'.format(i,','.join(names)))
