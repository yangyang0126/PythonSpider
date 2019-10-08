# -*- coding: utf-8 -*-
"""
Created on Tue May 14 14:59:25 2019

@author: YangYang
"""

from urllib.request import urlopen
import datetime
import re
import xlwt

# 定义保存Excel的位置
workbook = xlwt.Workbook()  #定义workbook
sheet = workbook.add_sheet('单词群打卡')  #添加sheet
head = ['扇贝ID', '扇贝用户名', '单词总计', '平均', '学习时间']    #表头
for h in range(len(head)):
    sheet.write(0, h, head[h])    #把表头写到Excel里面去

#计算打卡的统计时间
now = datetime.datetime.now()        #从今天开始查卡
#now = datetime.date(2019,5,13)      #输入查卡日期，自定义查卡日期
print("查卡日期：",now)
print('\n')
time2 = datetime.timedelta(days=8)   #统计一个星期的数据
day_now = str(now).split(" ")[0]
day_end = now - time2
day_end = str(day_end).split(" ")[0]

print("开始读取ID数据")
print("数据位置：")
print("C:/Users/Administrator/Desktop/user.txt")
print('\n')

#从txt导入数据
ID_total_input = open('C:/Users/Administrator/Desktop/user.txt')
ID_total = ID_total_input.read()
ID_total = ID_total.split("\n")  # 如果输入多个ID，用“\n”分开

i = 1  #定义Excel表格的行数，从第二行开始写入，第一行已经写了表头

for ID in ID_total:

    web = "https://www.shanbay.com/api/v1/checkin/user/"+str(ID)+"/"
    shanbay = urlopen(web)
    #shanbay = urlopen("https://www.shanbay.com/api/v1/checkin/user/16888030/")
    shanbay_data = shanbay.read().decode()
    
    #获取昵称
    find_username = re.findall("username\".*?,",shanbay_data)[0]
    username = str(find_username)[len("username\": \""):-2]
    
    # 获取打卡数据
    find_data = re.findall("\"stats\".*?track_object_img" ,shanbay_data)
    find_start = "\"stats\": "
    find_end = "\"track_object_img\""

    num_today = "\"num_today\": "
    used_time = "\"used_time\": "

    count = 0
    time_bdc = 0
    bdc_total = 0    
    
    #获取打卡天数
    checkin_time = []
    num_checkin_days = []
    find_checkin = re.findall("\"checkin_time\".*?\"share_urls\"",shanbay_data) 
    for checkin in find_checkin:
        shanbey_time = checkin.split(",")[0]
        shanbey_days = checkin.split(",")[3]
        checkin_time.append(str(shanbey_time)[len("\"checkin_time\": \""):len("\"checkin_time\": \"")+10])
        num_checkin_days.append(str(shanbey_days)[len("\"num_checkin_days\": "):])

    # 开始统计数据
    for data in find_data:       
    
        bdc = re.findall("\"bdc\":.*?}",data)
        if bdc == []:
            bdc = "{num_today\": 0, \"used_time\": 0.0}"    
    
        bdc_num = re.findall(r"\d+\.?\d*",str(bdc))[0]
        bdc_time = re.findall(r"\d+\.?\d*",str(bdc))[1]        
        
        if checkin_time[count] >= day_now:
            count += 1
        elif checkin_time[count] > day_end:            
            time_bdc = time_bdc+float(bdc_time)
            bdc_total = bdc_total+float(bdc_num)           
            #print("{}:打卡{}天,单词{}个,学习时间{}分钟".format(checkin_time[count],num_checkin_days[count],bdc_num,bdc_time))
            count += 1
        else:
            break
        
    average = bdc_total/7
    average = round(average,2)
    print("ID:{},昵称:{},背单词总计：{}，平均：{}，时长：{}分钟".format(ID,username,bdc_total,average,time_bdc))
    
    # 把内容保存到Excel
    sheet.write(i, 0, ID)  # 第i行，第1列
    sheet.write(i, 1, username)  # 第i行，第2列
    sheet.write(i, 2, bdc_total)  # 第i行，第3列
    sheet.write(i, 3, average)  # 第i行，第4列
    sheet.write(i, 4, time_bdc)  # 第i行，第5列
    i += 1

   # print(ID,username,bdc_total,average,time_bdc)

workbook.save('C:/Users/Administrator/Desktop/单词群打卡.xls')
print('\n') 
print('写入excel成功')
print("文件位置：")
print("C:/Users/Administrator/Desktop/单词群打卡.xls")
print('\n') 
input("查卡完毕，点击回车退出")  

