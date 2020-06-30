# -*- coding: utf-8 -*-
"""
Created on Mon Jun  3  2019

@author: YangYang
"""
import requests  # 获取网页数据
import datetime
import re
import xlwt

# 定义保存Excel的位置
workbook = xlwt.Workbook()  #定义workbook
sheet = workbook.add_sheet('单词打卡汇总')  #添加sheet
head = ['日期', '打卡天数','学习时间','学习内容']
for h in range(len(head)):
    sheet.write(0, h, head[h])    #把表头写到Excel里面去

#计算打卡的统计时间
now = datetime.datetime.now()        #从今天开始查卡
print("查卡日期：",now)
print('\n')
ID = 16888030
Pages = 20
day_end = datetime.date(2019,12,31)
day_end = str(day_end).split(" ")[0]


def WebRead(web):
    res = requests.get(web)  # requests发起请求，静态网页用get
    WebData = res.json()
    return WebData

ExcelRow = 1 
for Page in range(1,Pages):
    web = "https://www.shanbay.com/api/v1/checkin/user/"+str(ID)+"/"+"?page="+str(Page)
    WebData = WebRead(web) 
    for data in WebData['data']:       
        checkin_date = data['checkin_date']
        if checkin_date > day_end:
            num_checkin_days = data['num_checkin_days']
            try:
                info = data['info']                
                time = re.findall('\d+\.?\d*',info)[-1]      
            except:
                info = ''
                time = 5                    
            print("{}:打卡{}天,学习时间{}分钟,{}".format(checkin_date, num_checkin_days, time, info))     
            sheet.write(ExcelRow, 0, checkin_date)
            sheet.write(ExcelRow, 1, num_checkin_days)
            sheet.write(ExcelRow, 2, int(time))
            sheet.write(ExcelRow, 3, info)      
            ExcelRow += 1
        else:
            continue

workbook.save('扇贝打卡统计.xls')
print('\n') 
print('写入excel成功')

