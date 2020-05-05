# -*- coding: utf-8 -*-
"""
Created on Wed Nov 13 15:25:33 2019

@author: Yenny
"""

from selenium import webdriver
import  time
import xlwt

browser = webdriver.Chrome()
# 打开博客
browser.get('http://wap.cnki.net/touch/web/guide')
time.sleep(0.3)

# 进入搜索，输入主题
topic = "地下空间"
browser.find_element_by_id('btnSearch').click()
browser.find_element_by_id('keyword_ordinary').send_keys(topic)
browser.find_element_by_class_name('btn-search').click()
time.sleep(0.3)

# 筛选文献
browser.find_element_by_id("articletype_a").click()
time.sleep(0.3)
browser.find_element_by_css_selector("a[data-value=\"14\"]").click()

# 筛选学科
# browser.find_element_by_id("menu-toggle").click()
# browser.find_element_by_class_name('c-filter-title').click()

# 获取文献数量
num = browser.find_element_by_class_name('search-number').text
num = int(num[:-1])

# 加载所有页面
#for i in range(int(num/10)):
#    browser.find_element_by_class_name('c-company__body-item-more').click()
#    time.sleep(0.3)

#  加载3页
for i in range(3):
    browser.find_element_by_class_name('c-company__body-item-more').click()
    time.sleep(0.3)  
    
# 把网页拉到最下面，确保网页加载完成
# browser.find_element_by_class_name("c-footer__copyright").click()
# time.sleep(0.3)

# 获取文献信息
title = browser.find_elements_by_class_name('c-company__body-title')
author = browser.find_elements_by_class_name('c-company__body-author')
link = browser.find_elements_by_class_name('c-company-top-link')
content = browser.find_elements_by_class_name('c-company__body-content')
company = browser.find_elements_by_class_name('color-green')
info = browser.find_elements_by_class_name('c-company__body-info')

# 保存到Excel
# 定义保存Excel的位置
workbook = xlwt.Workbook()  #定义workbook
sheet = workbook.add_sheet(topic)  #添加sheet
head = ['标题', '作者', '摘要', '来源', '引用', '链接']    #表头
for h in range(len(head)):
    sheet.write(0, h, head[h])    #把表头写到Excel里面去
i = 1  #定义Excel表格的行数，从第二行开始写入，第一行已经写了表头    
for n in range(len(title)): 
    sheet.write(i, 0, title[n].text)
    sheet.write(i, 1, author[n].text)
    sheet.write(i, 2, content[n].text)
    sheet.write(i, 3, company[n].text)
    sheet.write(i, 4, info[n].text)
    sheet.write(i, 5, link[n].get_attribute('href'))    
    i += 1
workbook.save('知网文献汇总.xls')

# 关闭浏览器
browser.quit()