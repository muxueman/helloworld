# -*- coding: utf-8 -*-
"""
Created on Fri May 24 12:57:38 2019
display of simple/exponential moving average in terms of different parameters
@author: Stella
"""
import csv
from datetime import datetime
from matplotlib import pyplot as plt

def read_file():
    csv_file = 'AMD Historical Data.csv'
    dates, highs, lows, dailys, closes = [], [], [], [], []
    # 限制读取的数据量
    end_date = datetime.strptime("2019/4/13",'%Y/%m/%d')
    start_date = datetime.strptime("2018/1/11",'%Y/%m/%d')
    # 使用csv.reader读取csvfile中的文件
    with open(csv_file) as csvfile:
        csv_reader = csv.reader(csvfile)  
        stock_header = next(csv_reader) 
        for row in csv_reader: 
            date = datetime.strptime(row[0], '%Y/%m/%d')
            if (start_date < date and date < end_date):
                dates.append(date)
                highs.append(float(row[3]))
                lows.append(float(row[4]))
                closes.append(float(row[2]))
     # calculate average of close and open as a summary of a whole day
    for i in range(0, len(dates)):
        daily = (highs[i] + lows[i])/2
        dailys.append(daily)
    return dates, dailys, highs, lows
# N为moving average的计算天数，窗口长度
def simple_moving_average(N, dates, dailys):
    cumsum = 0
    moving_aves = []
    # simple moving average预处理
    for i in range(0, N):
        cumsum = cumsum + dailys[i]   
    # simple moving average
    for i in range(0, len(dates)):
        # 注意我们的数据在这里时间顺序是反的,所以反向计算moving averages
        if (i>0 and i< len(dates) - N + 1):
            cumsum = cumsum + dailys[i + N - 1] - dailys[i - 1]
        moving_aves.append(cumsum/N)
#    plt.plot(dates, moving_aves, label = N) 
    return moving_aves
# 0<a<1, 参数
def exponential_moving_average(a, N, dates, dailys):
    cumsum = 0
    verse_dates, verse_dailys, moving_aves = [], [],[]
    for date in reversed(dates):
        verse_dates.append(date)
    for daily in reversed(dailys):
        verse_dailys.append(daily)
    for i in range(0, N):
        cumsum = cumsum + verse_dailys[i]  
    ema = cumsum/N
    anticipate_moving = []
    for i in range(0, len(verse_dates)):
        if (i > N):
            ema = a*ema + (1 - a)*verse_dailys[i]
        moving_aves.append(ema)
        # anticpate trends in 10 days
    for i in range(0, len(moving_aves)):
        if (i < len(moving_aves)-4):
            anticipate_moving.append(moving_aves[i+4])
        else:
            anticipate_moving.append(anticipate_moving[i-1])
#    plt.plot(verse_dates, moving_aves, label = (a, N)) 
    plt.plot(verse_dates, anticipate_moving, label = (a, N)) 
    return verse_dates, moving_aves

def main():
    dates, dailys, highs, lows = read_file()
    # plot
#    print(dates)
#    print(dailys)
    plt.figure(dpi=128, figsize=(12, 5))
    plt.plot(dates, highs, c='yellow', alpha= 0.2)
    plt.fill_between(dates, highs, lows, facecolor = 'yellow', alpha = 0.4)
    plt.plot(dates, lows, c='yellow', alpha= 0.2)
#    moving_aves = simple_moving_average(10, dates, dailys) 
    #simple_moving_average(20)
    #simple_moving_average(40)
    exponential_moving_average(0.5, 20, dates, dailys)
    exponential_moving_average(0.8, 20, dates, dailys)
    exponential_moving_average(0.9, 20, dates, dailys)

    #plt.plot(dates, closes, label = "original") 
    #plt.title("Simple Moving Average of AMD: 2018/4/12 - 2019/4/12")
    plt.title("Exponential Moving Average of AMD: 2018/1/12 - 2019/4/12")
    plt.legend()
    plt.show()
    
if __name__ == '__main__':
	main()