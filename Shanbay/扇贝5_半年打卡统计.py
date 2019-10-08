# -*- coding: utf-8 -*-
"""
Created on Mon Jun  3  2019

@author: YangYang
"""
from urllib.request import urlopen
import datetime
import re
import xlwt

# 定义保存Excel的位置
workbook = xlwt.Workbook()  #定义workbook
sheet = workbook.add_sheet('单词打卡汇总')  #添加sheet
# head = ['扇贝ID', '扇贝用户名', '单词总计', '平均', '学习时间']    #表头
head = [ '日期', '打卡天数','单词','学习时间']
for h in range(len(head)):
    sheet.write(0, h, head[h])    #把表头写到Excel里面去

#计算打卡的统计时间
now = datetime.datetime.now()        #从今天开始查卡
#now = datetime.date(2019,5,13)      #输入查卡日期，自定义查卡日期
print("查卡日期：",now)
print('\n')
ID = 71256646
Pages = 15


i = 1  #定义Excel表格的行数，从第二行开始写入，第一行已经写了表头

def WebRead(web):
    WebResponse = urlopen(web)
    WebData = WebResponse.read().decode()
    return WebData

web1 = "https://www.shanbay.com/api/v1/checkin/user/"+str(ID)+"/"
shanbay_data = WebRead(web1)
    
#获取昵称
find_username = re.findall("username\".*?,",shanbay_data)[0]
username = str(find_username)[len("username\": \""):-2]

    
for Page in range(1,Pages):

    web = "https://www.shanbay.com/api/v1/checkin/user/"+str(ID)+"/"+"?page="+str(Page)
    shanbay_data = WebRead(web)    

    # 获取打卡数据
    find_data = re.findall("\"stats\".*?track_object_img" ,shanbay_data)
    find_start = "\"stats\": "
    find_end = "\"track_object_img\""

    num_today = "\"num_today\": "
    used_time = "\"used_time\": " 
    
    #获取打卡天数
    num_checkin_days = re.findall("num_checkin_days\": (.*?),",shanbay_data) 
    checkin_date = re.findall("\"checkin_date\": \"(.*?)\"",shanbay_data)

    count = 0
    # 开始统计数据
    for data in find_data:       
    
        bdc = re.findall("\"bdc\":.*?}",data)
        if bdc == []:
            bdc = "{num_today\": 0, \"used_time\": 0.0}"    
    
        bdc_num = re.findall(r"\d+\.?\d*",str(bdc))[0]
        bdc_time = re.findall(r"\d+\.?\d*",str(bdc))[1] 

        print("{}:打卡{}天,单词{}个,学习时间{}分钟".format(checkin_date[count],num_checkin_days[count],bdc_num,bdc_time))
        
        
        sheet.write(i, 0, checkin_date[count])
        sheet.write(i, 1, num_checkin_days[count])
        sheet.write(i, 2, bdc_num)
        sheet.write(i, 3, bdc_time)
        
        count += 1 
        
        i += 1

   # print(ID,username,bdc_total,average,time_bdc)

workbook.save('单词打卡统计.xls')
print('\n') 
print('写入excel成功')
print("文件位置：和代码在同一个文件夹")
print('\n') 
input("查卡完毕，点击回车退出")
