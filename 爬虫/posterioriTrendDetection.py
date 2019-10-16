# -*- coding: utf-8 -*-
"""
Created on Sun May 26 09:41:31 2019
trend and jump detection
@author: Stella
"""
from matplotlib import pyplot as plt
import pandas
import numpy 
import movingAverage
# adjust the data in sequence of ascending from descending
def verse(list):
    verse_list, useful_list = [], []
    for ele in reversed(list):
        verse_list.append(ele)
    for i in range(0, len(verse_list)):
        if(i > 40):
            useful_list.append(verse_list[i])
    return useful_list

# up_trend = 1, down_trend = -1
def trend(f, T):
    trends = numpy.zeros(len(f))
    adjust_trends, anticipate_trends = [], []
    for i in f.index:
        if(f.A_10[i] > f.A_20[i] and f.A_20[i] > f.A_40[i]):
            trends[i] = 1
        if(f.A_10[i] < f.A_20[i] and f.A_20[i] < f.A_40[i]):
            trends[i] = -1 
    # anticpate trends in 10 days
    for i in range(0, len(trends)):
        if (i < len(trends)-10):
            anticipate_trends.append(trends[i+10])
        else:
            anticipate_trends.append(0)
#    plt.plot(f.dates, trends, c='blue', alpha= 1, label = 'original trend')
    # remove trends that are less than T days
    for i in range (0, len(trends)):
        if (i < len(trends)-T+1 and i > 0):
            less = 0
            for j in range(1, T):
                if (anticipate_trends[i+j] != anticipate_trends[i]):
                    less = 1
            if(less == 1):
                adjust_trends.append(adjust_trends[i-1]) 
            else:
                adjust_trends.append(anticipate_trends[i])
        else:
            adjust_trends.append(anticipate_trends[i]) 
# reduce no-trend if it is less than 10 days
    for i in range(1 ,len(adjust_trends)-10):
        if (adjust_trends[i] == 0):
            num = 0
            for j in range(1, 10):
                if (adjust_trends[i+j] == 0):
                    num+=1
            if (num < 7):
                adjust_trends[i] = adjust_trends[i-1]   
    return adjust_trends    
# number of significant jumps 
def num_jumps(jumps):
    num = 0
    for jump in jumps:
        if(jump != 0):
            num+=1
    return num
#up_jump = 1, down_jump = -1
def jump(f, x, y):
    jumps = numpy.zeros(len(f))
    for i in range(4, len(f)-4):
        if(f.A_3[i+3] < (f.A_3[i-1]*(1-x)) and f.A_5[i+4] < (f.A_5[i-2]*(1-y))):
            jumps[i] = -1
        if(f.A_3[i+3] > (f.A_3[i-1]*(1+x)) and f.A_5[i+4] > (f.A_5[i-2]*(1+y))):
            jumps[i] = 1
    print("number of original jumps: ", num_jumps(jumps))
#    adjust jumps, remove the following
    for i in range(0, len(jumps)):
        if (jumps[i] != 0 and f.trends[i] == 0):
            jumps[i] = 0
    print("number of jumps after delete conjestion jumps: ", num_jumps(jumps))        
    for i in range(0, len(jumps)):
        if(jumps[i] != 0):
            j = 1
            while (jumps[i+j] == jumps[i]):
                jumps[i+j] = 0
                j = j + 1
    print("number of jumps after delete same jumps: ", num_jumps(jumps))       
    for i in range(0, len(jumps) - 9):
        for j in range(1, 9):
            if (jumps[i] != 0 and jumps[i+j] == jumps[i]):
                jumps[i+j] = 0
    print("number of jumps after delete nearby jumps: ", num_jumps(jumps))    
    for i in range(0, len(jumps)-5):
        if (jumps[i] != 0):
            for j in range(1, 5):
                if (jumps[i+j] != 0):
                    jumps[i] = 0
    print("number of jumps after delete contradictory jumps: ", num_jumps(jumps))        
    for i in range(0, len(jumps)):
        if(jumps[i] != 0 and abs(f.dailys[i-2] - f.dailys[i+2]) < 0.3):
            jumps[i] = 0
    print("number of jumps after delete small jumps: ", num_jumps(jumps))       
    return jumps

def plot_jumps(f):
    for i in range(0, len(f)):
        if (f.jumps[i] == 1):
            plt.scatter(f.dates[i], f.dailys[i], c = 'red')
        if (f.jumps[i] == -1):
            plt.scatter(f.dates[i], f.dailys[i], c = 'green')
        
        
def main():
    # create dataFrame to store data
    fig = plt.figure(dpi=128, figsize=(16, 5))
    dates, dailys, highs, lows = movingAverage.read_file()
    f = pandas.DataFrame({'dates':verse(dates),'dailys':verse(dailys)})
    f['A_3'] = verse(movingAverage.simple_moving_average(3, dates, dailys))
    f['A_5'] = verse(movingAverage.simple_moving_average(5, dates, dailys))
    f['A_10'] = verse(movingAverage.simple_moving_average(10, dates, dailys))
    f['A_20'] = verse(movingAverage.simple_moving_average(20, dates, dailys))
    f['A_40'] = verse(movingAverage.simple_moving_average(30, dates, dailys))
    f['trends'] = trend(f, 7)
    f['jumps'] = jump(f, 0.07, 0.056)
    plot_jumps(f)           
    #print(f[['dates', 'dailys', 'trends', 'jumps']])
    plt.plot(f.dates, f.dailys, c='black')
    plt.plot(f.dates, f.trends, c='black', label = 'more than 7 bussiness day trend')
    plt.legend()
    plt.grid(ls='--')
    plt.title("AMD: 2008/6 - 2011/4")
    plt.show()
    
if __name__ == '__main__':
	main()