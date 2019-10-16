# -*- coding: utf-8 -*-

"""
Created on Sat May 11 09:53:53 2019
orginal code for dowloading the historical stock data of S&P 500 companies in United States
mainly using selenium, webdriver, xpath methods
@author: Stella
"""
from selenium import webdriver
from selenium.webdriver.support.select import Select
from lxml import etree
import time

id_list = []
#name_list = []
#解析页面 获取company的信息
def parse_page_source(content):
    # 生成对象
    tree = etree.HTML(content)
    # 抓取内容
    company_list = tree.xpath('//div[@id="marketInnerContent"]//tbody//tr')
    # 遍历div列表
    for company in company_list:
        company_id = company.xpath('.//a/@href')
#        company_name = company.xpath('.//a//text()')
#        name_list.append(company_name)
        id_list.append(company_id)
    return id_list
## 创建一个参数对象，用来控制chrome以无界面模式打开
#chrome_options = Options()
#chrome_options.add_argument('--headless')
#chrome_options.add_argument('--disable-gpu')
#browser = webdriver.Chrome(executable_path=path, chrome_options=chrome_options)
# 处理弹出的警告页面 accept()  dismiss()
#browser.switch_to_alert().accept()
#sleep(2)
# 储存页面数据
#with open(r'python.html', 'w', encoding='utf8') as fp:
#	fp.write(browser.page_source)
def main():
	# 模拟创建一个浏览器对象，然后让对象去操作浏览器
    path = r'C:\Users\Stella\Desktop\ProjectPython\chromedriver.exe'
    browser = webdriver.Chrome(executable_path = path)
    # 通过浏览器打开网页
    url = 'https://www.investing.com/equities/united-states'
    browser.get(url)
    handle = browser.current_window_handle
    # 发送请求和响应是需要时间的
    time.sleep(2)
    # 登陆login
    browser.find_element_by_xpath('//div[@class="topBarText"]/a[1]').click()
    time.sleep(2)
    browser.find_element_by_id('loginFormUser_email').send_keys('stellamuxueman@hotmail.com')
    browser.find_element_by_id('loginForm_password').send_keys('Apple124')
    browser.find_element_by_xpath('//div[@id="signup"]//a[@class="newButton orange"]').click()
    time.sleep(2)
    # 查找'S&P 500'selectBox框,利用Select模块处理下拉框
    my_select_option = browser.find_element_by_id('stocksFilter')
    Select(my_select_option).select_by_visible_text("S&P 500")
    time.sleep(2)
    # 获取页面信息
    page_source = browser.page_source
    # 解析信息 获取company list
    id_list = parse_page_source(page_source)
    # 打开每个company页面 选择时间并下载数据
    for company_id in id_list:
        # 转化参数格式
        company_id = company_id.__str__()
        company_id = company_id.split('\'')[1]
        # 构建新页面的链接地址
        company_url = 'https://www.investing.com' + company_id + '-historical-data'
        # 新建标签页打开
        js='window.open("'+ company_url +'");'
        print(js)
        browser.execute_script(js)   
#       获取所有的窗口
        handles = browser.window_handles
        # 对窗口进行遍历
        for newhandle in handles:
#           筛选新打开的窗口
            if (newhandle!=handle):
                if (newhandle !=handles[1]):
#                   切换指定的窗口打开
                    browser.switch_to.window(handles[2])
                    time.sleep(1)
#                   拖动到可见的元素去 下拉页面
#                   target = driver.find_element_by_id("id_keypair")
#                   driver.execute_script("arguments[0].scrollIntoView();", target)
#                   使用js脚本直接操作 下拉页面 
#                   否则报错ElementNotVisibleException: element not interactable
                    js="var q=document.documentElement.scrollTop=200"
                    browser.execute_script(js)
                    time.sleep(1)
#                   选择历史数据时间并下载数据
                    browser.find_element_by_id('widgetFieldDateRange').click()
                    date_start = browser.find_element_by_id('startDate')
                    date_start.clear()
                    date_start.send_keys("05/25/2008")
                    date_end = browser.find_element_by_id('endDate')
                    date_end.clear()
                    date_end.send_keys("05/25/2019")
                    time.sleep(1)
                    browser.find_element_by_id('applyBtn').click()
                    # 这里必须停5秒 加载是需要时间的
                    time.sleep(5)
                    browser.find_element_by_xpath('//div[@id="column-content"]//div/a').click()
                    time.sleep(2) 
                    #关闭标签页
                    browser.close()
                    # 回到主页面
                    browser.switch_to.window(handle)              
    time.sleep(2)
    # 关闭浏览器
    browser.quit()

if __name__ == '__main__':
	main()