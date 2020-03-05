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
DayMon = str(datetime.datetime.now() - datetime.timedelta(days=7)).split(" ")[0]  
DayTue = str(datetime.datetime.now() - datetime.timedelta(days=6)).split(" ")[0]  
DayWed = str(datetime.datetime.now() - datetime.timedelta(days=5)).split(" ")[0]  
DayThur = str(datetime.datetime.now() - datetime.timedelta(days=4)).split(" ")[0]  
DayFri = str(datetime.datetime.now() - datetime.timedelta(days=3)).split(" ")[0]  
DaySat = str(datetime.datetime.now() - datetime.timedelta(days=2)).split(" ")[0] 
DaySun = str(datetime.datetime.now() - datetime.timedelta(days=1)).split(" ")[0]  
DayEnd = str(datetime.datetime.now() - datetime.timedelta(days=8)).split(" ")[0]  

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
head = ['ID', 'NickName', DayMon, DayTue, DayWed, DayThur, DayFri, DaySat, DaySun,'打卡天数','单词总计', '时间总计']    #表头
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

def CollectCheakinBDC(i,day,LearningDataDaily,style1,style2):
    global bdc_used_time_total,bdc_num_today_total,checkin_date_total
    try:
        bdc_num_today = LearningDataDaily['stats']['bdc']['num_today']
        bdc_used_time = LearningDataDaily['stats']['bdc']['used_time']
        if bdc_num_today<20 or bdc_used_time<6:
            sheet.write(i, day, str(bdc_num_today)+"/"+str(bdc_used_time),style1)
        else:
            sheet.write(i, day, str(bdc_num_today)+"/"+str(bdc_used_time),style2)
        bdc_used_time_total += bdc_used_time
        bdc_num_today_total += bdc_num_today
        checkin_date_total += 1
    except:  
        bdc_num_today = 0
        bdc_used_time = 0.0
        bdc_used_time_total = bdc_used_time_total
        bdc_num_today_total = bdc_num_today_total
        checkin_date_total = checkin_date_total
    return bdc_used_time_total,bdc_num_today_total,checkin_date_total

for ID in ID_total:
    
    web = "https://www.shanbay.com/api/v1/checkin/user/"+str(ID)+"/"
    res = requests.get(web)  # requests发起请求，静态网页用get
    LearningData = res.json()
    sheet.write(i, 0, ID,style2) # 保存ID
    NickName = LearningData['data'][0]['user']['nickname']
    sheet.write(i, 1, NickName, style2) # 保存昵称

    bdc_used_time_total = 0
    checkin_date_total = 0
    bdc_num_today_total = 0
    # 获取单词打卡记录
    for LearningDataDaily in LearningData['data']:
        checkin_date =  LearningDataDaily['checkin_date']
        if checkin_date == DayMon:
            CollectCheakinBDC(i,2,LearningDataDaily,style1,style2)
        if checkin_date == DayTue:
            CollectCheakinBDC(i,3,LearningDataDaily,style1,style2)
        if checkin_date == DayWed:
            CollectCheakinBDC(i,4,LearningDataDaily,style1,style2)
        if checkin_date == DayThur:
            CollectCheakinBDC(i,5,LearningDataDaily,style1,style2)         
        if checkin_date == DayFri:
            CollectCheakinBDC(i,6,LearningDataDaily,style1,style2)
        if checkin_date == DaySat:
            CollectCheakinBDC(i,7,LearningDataDaily,style1,style2)
        if checkin_date == DaySun:
            CollectCheakinBDC(i,8,LearningDataDaily,style1,style2)
    if checkin_date_total<5:
        sheet.write(i, 9, checkin_date_total,style1)
    else:
        sheet.write(i, 9, checkin_date_total,style2)
    sheet.write(i, 10, bdc_num_today_total,style2)
    sheet.write(i, 11, bdc_used_time_total,style2)
    print(ID+","+NickName+"打卡"+str(checkin_date_total)+"天，单词总计"+str(bdc_num_today_total)+"个")
    i += 1 

<<<<<<< HEAD
workbook.save('C:/Users/zhaoy/单词群打卡.xls')
=======
workbook.save('C:/Users/admin/Desktop/单词群打卡.xls')
>>>>>>> 1b6f24b6675f8f26766c8851f3297753ca6cb7ed
print('\n') 
print('写入excel成功')
print("文件位置：")
print("C:/Users/Administrator/Desktop/单词群打卡.xls")
print('\n') 
input("查卡完毕，点击回车退出")  
