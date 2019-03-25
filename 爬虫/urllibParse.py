# -*- coding: utf-8 -*-
"""
Created on Mon Mar 25 11:26:02 2019

quote, unquote
urlencode

@author: Stella
"""

import urllib.parse

image_url = 'https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1553518891279&di=33507889414a2bad64b6f3209a0b7050&imgtype=0&src=http%3A%2F%2F01imgmini.eastday.com%2Fmobile%2F20190227%2F20190227105459_b3ea948b67694f56ab26ab4e39c49afc_1.jpeg'
#url 只能用特定的字符组成，字母、数字、下划线
#如果出现其他字符，比如￥ 空格 中文，就要对其进行编码





##url quote编码解码函数
#url = 'http://www.baidu.com/index.html?name=邓超元&pwd=123456'

#ret = urllib.parse.quote(url)
#re = urllib.parse.unquote(ret)
#
#print(ret) #可以编码解码
#print(re)





#用字典的方法拼接url
url= 'http://www.baidu.com/index.html'
#假如参数有 name, age, sex, height
name = 'dengchaoyuan'
age = 18
sex = 'male'
height = '180'

#url = 'http://www.baidu.com/index.html?name=dengchaoyuan&age=18&sex=male&height=180'

data = {
        'name': name,
        'age': age,
        'sex': sex,
        'height': height,
}

#遍历字典

#方法1 自己写
#lt =[]
#for k,v in data.items():
#    lt.append(k + '=' +str(v))
#query_string = '&'.join(lt)

#方法2 提供封装好的代码，并且特殊字符如中文编码了
query_string = urllib.parse.urlencode(data)
print(query_string)

url = url + '?' + query_string

print(url)



