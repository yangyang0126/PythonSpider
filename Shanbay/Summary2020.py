# -*- coding: utf-8 -*-
"""
Created on Thu Mar  5 14:46:04 2020

@author: admin
"""
import requests  # 获取网页数据
import datetime
import xlwt
import pandas as pd
import pygal
  
# 准备表格
workbook = xlwt.Workbook()  #定义workbook
sheet = workbook.add_sheet('2020')  #添加sheet
head = ['date', 'bdc','listen','read','time_bdc','time_listen','time_read']
for h in range(len(head)):
    sheet.write(0, h, head[h])    #把表头写到Excel里面去
ExcelRow = 1; #定义Excel表格的行数，从第二行开始写入，第一行已经写了表头

# 读取数据
ID = 16888030
for Page in range(1,10):
    Web = "https://www.shanbay.com/api/v1/checkin/user/"+str(ID)+"/"+"?page="+str(Page)
    Res = requests.get(Web)
    DataEveryPage = Res.json()
    
    End = str(datetime.date(2020,1,1)).split(" ")[0]   
    
    for data in DataEveryPage['data']:
        if data['info']!='':
            if data['checkin_date'] >= End:
                sheet.write(ExcelRow, 0, data['checkin_date'])  
                try:
                    sheet.write(ExcelRow, 1, data['stats']['bdc']['num_today'])
                    sheet.write(ExcelRow, 4, data['stats']['bdc']['used_time'])                   
                except:
                    sheet.write(ExcelRow, 1, 0) 
                    
                try:
                    sheet.write(ExcelRow, 2, data['stats']['listen']['num_today'])
                    sheet.write(ExcelRow, 5, data['stats']['listen']['used_time'])                   
                except:
                    sheet.write(ExcelRow, 2, 0)  
                    sheet.write(ExcelRow, 5, 0)  
                    
                try:
                    sheet.write(ExcelRow, 3, data['stats']['read']['num_today'])
                    sheet.write(ExcelRow, 6, data['stats']['read']['used_time'])                   
                except:
                    sheet.write(ExcelRow, 3, 0)  
                    sheet.write(ExcelRow, 6, 0)       
                ExcelRow += 1
            else:
                break
workbook.save('Summary2020.xls')
input("查卡完毕，点击回车退出")

# 汇总数据，pandas
df = pd.read_excel('Summary2020.xls')
df['date'] = pd.to_datetime(df['date']) 
df = df.set_index('date') # 将date设置为index
MonthDf = df.resample('M').sum().head()

# 绘图
<<<<<<< HEAD
MonthDf['bdc'][1]
line_chart = pygal.StackedBar()
line_chart.title = 'Browser usage evolution (in %)'
line_chart.x_labels = map(str, range(2002, 2013))
line_chart.add('Firefox', [None, None, 0, 16.6,   25,   31, 36.4, 45.5, 46.3, 42.8, 37.1])
line_chart.add('Chrome',  [None, None, None, None, None, None,    0,  3.9, 10.8, 23.8, 35.3])
line_chart.add('IE',      [85.8, 84.6, 84.7, 74.5,   66, 58.6, 54.7, 44.8, 36.2, 26.6, 20.1])
line_chart.add('Others',  [14.2, 15.4, 15.3,  8.9,    9, 10.4,  8.9,  5.8,  6.7,  6.8,  7.5])
line_chart.render_to_file('bar_chart.svg')         
=======

line_chart = pygal.StackedBar()
line_chart.title = ''
line_chart.x_labels = map(str, range(1, 13))
line_chart.add('bdc', MonthDf['time_bdc'])
line_chart.add('listen', MonthDf['time_listen'])
line_chart.add('read', MonthDf['time_read'])
line_chart.add('speak', [450,450,450])
line_chart.render_to_file('summary.svg')         
>>>>>>> b8ecd6bbd21d041340c65efb72ce7f0e035d730f
