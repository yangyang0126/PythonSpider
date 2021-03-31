# -*- coding: utf-8 -*-
"""
Created on Thu Jan 28 14:08:18 2021

@author: zhaoy
"""

import requests  # 获取网页数据
import datetime
import xlwt
  
# 准备表格
workbook = xlwt.Workbook()  #定义workbook
sheet = workbook.add_sheet('2020')  #添加sheet
head = ['date', 'bdc','listen','read','time_bdc','time_listen','time_read']
for h in range(len(head)):
    sheet.write(0, h, head[h])    #把表头写到Excel里面去
ExcelRow = 1; #定义Excel表格的行数，从第二行开始写入，第一行已经写了表头

# 读取数据
ID = 16888030
for Page in range(1,2):
    Web = "https://www.shanbay.com/api/v1/checkin/user/"+str(ID)+"/"+"?page="+str(Page)   
    Res = requests.get(Web)
    print(Res)
    DataEveryPage = Res.json()
    
    End = str(datetime.date(2021,1,1)).split(" ")[0]   
    
    for data in DataEveryPage['data']:
        if data['info']!='':
            if data['checkin_date'] >= End:
                sheet.write(ExcelRow, 0, data['checkin_date'])  
                print(data['checkin_date'])
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
workbook.save('Summary20210128.xls')
input("查卡完毕，点击回车退出")