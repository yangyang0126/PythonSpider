# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 14:09:51 2020
@author: Yenny
"""
from selenium import webdriver
#import  time
import xlwt
workbook = xlwt.Workbook()  #定义workbook
sheet = workbook.add_sheet('记录')  #添加sheet
row = 0


for page in range(32,50):
    web = 'http://www.cbirc.gov.cn/cn/view/pages/ItemList.html?itemPId=923&itemId=4114&itemUrl=ItemListRightList.html&itemName=银保监局本级&itemsubPId=931&itemsubPName=行政处罚#'+str(page)
    browser = webdriver.Chrome()
    browser.get(web)  
    
    # 获取当页所有链接目录
    part = browser.find_elements_by_class_name('caidan-right-list') 
    link0 = part[0].find_elements_by_class_name('title')
    date0 = part[0].find_elements_by_class_name('date')
    link1 = part[1].find_elements_by_class_name('title')
    date1 = part[1].find_elements_by_class_name('date')
    link2 = part[2].find_elements_by_class_name('title')
    date2 = part[2].find_elements_by_class_name('date')
    
    # 获取链接详情和标题
    link_name = []
    link_url = []  
    link_date = []
    for i in range(18):        
        a = link0[i].find_elements_by_tag_name('a')
        link_url.append(a[0].get_attribute("href"))
        
    for i in range(6):
        link_date.append(date0[i].text)
        link_name.append(link0[i].text)                
    for i in range(6,12):
        link_date.append(date1[i].text)
        link_name.append(link1[i].text)        
    for i in range(12,18):
        link_date.append(date2[i].text)
        link_name.append(link2[i].text)    
       
    for i in range(18):   
        column = 2 
        sheet.write(row, 0, link_date[i])  # 输入日期        
        sheet.write(row, 1, link_name[i])  # 输入标题
                
        browser.get(link_url[i]) 
        handle = browser.current_window_handle
        browser.switch_to_window(handle)    
        
        list_detail = browser.find_elements_by_class_name('MsoNormal')
        if list_detail == []:
            list_detail = browser.find_elements_by_class_name('p0')
            
        for j in range(len(list_detail)):            
            sheet.write(row, column, list_detail[j].text)            
            column += 1
            
        row += 1          
    
    browser.quit()
    
workbook.save('aa.xls')
