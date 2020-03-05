# -*- coding: utf-8 -*-
"""
Created on Mon May 20 11:50:05 2019

@author: Yenny
"""


import datetime # 计算时间
import xlwt # 保存Excel
import os # 获取文件路劲
import requests  # 获取网页数据

#计算打卡的统计时间
DayToday = str(datetime.datetime.now()).split(" ")[0]
# now = datetime.date(2019,9,9)      # 输入查卡日期，自定义查卡日期
print("查卡日期：",DayToday)
print('\n')
DayCheck = str(datetime.datetime.now() - datetime.timedelta(days=1)).split(" ")[0]  

# 定义保存Excel的位置
workbook = xlwt.Workbook()  #定义workbook
sheet = workbook.add_sheet(DayToday)  #添加sheet

# 设置居中
al = xlwt.Alignment()
al.horz = 0x02      # 设置水平居中
al.vert = 0x01      # 设置垂直居中

# 设置边框
borders = xlwt.Borders() # Create Borders
borders.left = xlwt.Borders.THIN 
borders.right = xlwt.Borders.THIN
borders.top = xlwt.Borders.THIN
borders.bottom = xlwt.Borders.THIN
borders.left_colour = 0x40
borders.right_colour = 0x40
borders.top_colour = 0x40
borders.bottom_colour = 0x40

# 设置单元格背景颜色
pattern = xlwt.Pattern() 
pattern.pattern = xlwt.Pattern.SOLID_PATTERN 
pattern.pattern_fore_colour = 47


# 创建样式
style1 = xlwt.XFStyle()  # 创建一个样式对象，初始化样式 style1
style2 = xlwt.XFStyle()  # 创建一个样式对象，初始化样式 style2

style1.borders = borders # Add Borders to Style
style2.borders = borders # Add Borders to Style
style1.alignment = al
style2.alignment = al
style1.pattern = pattern # Add Pattern to Style

# 写入数据
head = ['ID', '打卡详情']    #表头
for h in range(len(head)):
    sheet.write(0, h, head[h],style2)    #把表头写到Excel里面去

    
path = os.getcwd() # 获取当前代码文件路径
print("开始读取ID数据")
print("数据位置："+ path+"ID.txt")
print('\n')

#从txt导入数据
ID_total_input = open('ID.txt')
ID_total = ID_total_input.read()
ID_total = ID_total.split("\n")  # 如果输入多个ID，用“\n”分开

i = 1  #定义Excel表格的行数，从第二行开始写入，第一行已经写了表头

for ID in ID_total:
    
    web = "https://www.shanbay.com/api/v1/checkin/user/"+str(ID)+"/"
    res = requests.get(web)  # requests发起请求，静态网页用get
    LearningData = res.json()
    sheet.write(i, 0, ID,style2) # 保存ID
    NickName = LearningData['data'][0]['user']['nickname']
    

    bdc_used_time_total = 0
    checkin_date_total = 0
    bdc_num_today_total = 0
    # 获取单词打卡记录
    for LearningDataDaily in LearningData['data']:
        checkin_date =  LearningDataDaily['checkin_date']
        if checkin_date == DayCheck:
            sheet.write(i, 1, NickName+LearningDataDaily['info'], style2) # 保存打卡数据        
            print(NickName,LearningDataDaily['info'])
            break        
    i += 1 

workbook.save('打卡排行榜.xls')
print('\n') 
print('写入excel成功')
print("文件位置：")
print("C:/Users/Administrator/Desktop/打卡排行榜.xls")
print('\n') 
input("查卡完毕，点击回车退出")  
