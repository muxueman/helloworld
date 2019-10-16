# -*- coding: utf-8 -*-
"""
Created on Mon May 20 15:57:59 2019
introducing the turning point method to reduce demension of raw data from MySQL
@author: Stella
"""
#pip install mysql-connector-python

import mysql.connector
import matplotlib.pyplot as plt
plt.rcParams['figure.figsize'] = (16.0, 4.0)
plt.rcParams['savefig.dpi'] = 600 #图片像素
plt.rcParams['figure.dpi'] = 600 #分辨率
# value and date of the time series
value = []
date = []
# conntect to MySQL
conn = mysql.connector.connect(host='localhost', user='root', password='Apple124', database='historical_data')
cursor = conn.cursor()
# import data from MySQL
#cursor.execute('select date from amd_historical_data') 
cursor.execute('select date from amd_historical_data limit 300') 
date = cursor.fetchall()
#cursor.execute('select close from amd_historical_data') 
cursor.execute('select close from amd_historical_data limit 300') 
value = cursor.fetchall()
# transfer the original string data of tuples into integer
for v in range (0, len(value)):
    value[v] = str(value[v])
    value[v] = value[v].replace(',', '').replace('(', '').replace(')', '').replace('\'', '')
    value[v] = float(value[v])
print("totoal number of data: ",len(value))
plt.plot(date, value, label='original')
# iterator level
N = 6
# value and date of the local minimum ana maximum
extrema_value = []
extrema_date = []
# value and date of N level of deepness of the time series, the N-level turning points
turning_value = []
turning_date = []
# delete the value who has the same value of the previous one
# this makes sure that we won't get stuck in flat pattern
removes = list([])
for i in range (0, len(value) - 1):
    if(value[i] == value[i + 1]):
        removes.append(i + 1)
for j in range (0, len(removes)):
    del value[removes[j] - j]
    del date[removes[j] - j]
print("after removing same adjacent data: ",len(value))
# find extremum
extrema_value.append(value[0])
extrema_date.append(date[0])
for k in range (1, len(value) - 1 ):
    if(k != len(value) - 1):
        if((value[k] <= value[k - 1]) and (value[k] <= value[k + 1])):
            extrema_value.append(value[k])
            extrema_date.append(date[k])
        if ((value[k] >= value[k - 1]) and (value[k] >= value[k + 1])):
            extrema_value.append(value[k])
            extrema_date.append(date[k])
    else:
            extrema_value.append(value[k])
            extrema_date.append(date[k])
print("total extremum: ",len(extrema_value))
#plt.plot(extrema_date, extrema_value, label='extremum')
# first level of turning points, thus extremum
turning_value = list(extrema_value)
turning_date = list(extrema_date)
# find N-level turning points
for n in range (0, N):
    # store temp index of those values
    temp = []
    a = 0
    while (a < len(turning_value) - 3): 
        if (turning_value[a] < turning_value[a + 1] and turning_value[a] < turning_value[a + 2] and turning_value[a + 1] < turning_value[a + 3] and turning_value[a + 2] < turning_value[a + 3] and (abs(turning_value[a + 1] - turning_value[a + 2]) < (abs(turning_value[a] - turning_value[a + 2]) + abs(turning_value[a + 1] - turning_value[a + 3])))):
            temp.append(a + 1) 
            temp.append(a + 2) 
            a = a + 3 
        elif (turning_value[a] > turning_value[a + 1] and turning_value[a] > turning_value[a + 2] and turning_value[a + 1] > turning_value[a + 3] and turning_value[a + 2] > turning_value[a + 3] and (abs(turning_value[a + 1] - turning_value[a + 2]) < (abs(turning_value[a] - turning_value[a + 2]) + abs(turning_value[a + 1] - turning_value[a + 3])))): 
            temp.append(a + 1) 
            temp.append(a + 2) 
            a = a + 3    
        elif (turning_value[a + 1] == turning_value[a + 3] and turning_value[a] == turning_value[a + 2]): 
            temp.append(a + 1) 
            temp.append(a + 2) 
            a = a + 3 
        else: 
            a = a + 1 
    # delete the flattened points 
    for m in range(0, len(temp)): 
        del turning_value[temp[m] - m] 
        del turning_date[temp[m] - m]
    print("the ", n+1, " level turning points: ",len(turning_value))

#plt.plot(turning_date, turning_value, label='turning point')
#plt.title("AMD: 2008/4/14 - 2019/4/12")
plt.xlabel('date')
plt.ylabel('price')
plt.xticks([]) 
plt.legend()
#plt.savefig('amd_historical_300.png')
plt.show()