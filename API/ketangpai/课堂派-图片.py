# -*- coding: utf-8 -*-
"""
Created on Mon Nov 11 13:02:43 2019

@author: Administrator
"""
import requests

#从txt导入数据
page_url = open('a.txt').read()
urls = page_url.split("\n")  # 如果输入多个ID，用“\n”分开

page = 0  # PDF页面

headers = {
    
    "user-agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"

}

for url in urls:
    print("正在取读"+str(page))
    wb =  requests.get("https://document.ketangpai.com/img/"+url, headers=headers)   
    content = wb.content #获取页面内容
    title = str(page) + ".jpg"
    fp = open(title,"ab") #打开一个文本文件
    fp.write(content) #写入数据
    fp.close() #关闭文件
    page += 1