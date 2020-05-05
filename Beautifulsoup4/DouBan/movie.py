# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 14:40:03 2020

@author: zhaoy
"""

import requests  
from bs4 import BeautifulSoup  # 导入BeautifulSoup
import xlwt  # 把Excel输出模块加进来

# 定义保存Excel的位置
workbook = xlwt.Workbook()  # 定义workbook
sheet = workbook.add_sheet('数据')  # 添加sheet
head = ['年份', '电影名称', '豆瓣评分', '评价人数', '推荐理由', '电影链接'] # 表头
for h in range(len(head)):
    sheet.write(0, h, head[h])    # 把表头写到Excel里面去，从0开始

def GetRes(url):     
    headers = {
      'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
    }
    res = requests.get(url, headers=headers)  
    soup = BeautifulSoup(res.text, 'html.parser') 
    return soup

url = 'https://movie.douban.com/top250?start={}&filter='
urls = [url.format(num * 25) for num in range(10)]
row = 1 # excel表格的行
for page in urls:
    soup = GetRes(page)
    items = soup.select('ol.grid_view div.item')
    for i in items:
        title = i.select('span.title')[0].text
        link = i.find('a')['href']
        rate = i.find('div',class_='star').text.split('\n')[2]
        number = i.find('div',class_='star').text.split('\n')[-2]
        try:
            quote = i.select('p.quote')[0].text.split('\n')[1]
        except:
            quote = ""    # 有些电影没有推荐语     
        year = i.find('p', class_="").text.split('\n')[2].strip()[:4]
        print(row,title)
        # 把内容保存到Excel
        sheet.write(row, 0, year)  
        sheet.write(row, 1, title)  
        sheet.write(row, 2, rate) 
        sheet.write(row, 3, number)  
        sheet.write(row, 4, quote)  
        sheet.write(row, 5, link)  
        row += 1

# 保存Excel表
workbook.save('豆瓣电影排行榜.xls')  
print('写入excel成功')