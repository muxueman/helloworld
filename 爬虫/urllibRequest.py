# -*- coding: utf-8 -*-
"""
Created on Fri Mar 22 09:52:32 2019

urlopen
抓包工具的使用

@author: Stella
"""

#import urllib.parse
import urllib.request

#url = 'http://www.baidu.com'
##完整的url:http://www.baidu.com:80/index.html?name=manman&password=123#lala
#response=urllib.request.urlopen(url)

#print(response)
#print(response.read())
#print(response.read().decode())
#print(response.geturl())
#print(dict(response.getheaders())) 转成字典，获取头部信息,列表里面有元组
#print(response.getcode()) 获取状态码
#print(response.readlines()) 返回列表都是字节类型

#with open('baidu.html','w',encoding='utf8') as fp:
#    fp.write(response.read().decode())
    
#with open('baidu1.html','wb') as fp:
#    fp.write(response.read())








#下载图片

image_url='https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1553518891280&di=32c7bc9fc0c6d5493ffeb999970cb4bb&imgtype=0&src=http%3A%2F%2Fwxt.sinaimg.cn%2Fthumb300%2F0077Pisegy1g01s8kda7eg30fa0fanpg.gif%3Ftags%3D%255B%255D'

response=urllib.request.urlopen(image_url) #字符串格式
#像图片只能写入本地二进制的格式
with open('yuanyuan.jpg','wb') as fp:
    fp.write(response.read())


#方法2
#urllib.request.urlretrieve(image_url,'yuanyuan2.jpg')











