ai # -*- coding: utf-8 -*-
"""
Created on Tue May 14 17:47:05 2019

@author: YangYang
"""

# 针对扇贝打卡数据统计和分析
# 只统计 单词、炼句、听力、阅读 四部分的数据，阅读不区分短语和文章

from urllib.request import urlopen
import datetime
import re
import xlwt

# 定义保存Excel的位置
workbook = xlwt.Workbook()  #定义workbook
sheet = workbook.add_sheet('本周打卡')  #添加sheet
head = ['打卡', '单词', '阅读', '炼句', '听力', '学习时间']    #表头
for h in range(len(head)):
    sheet.write(0, h, head[h])    #把表头写到Excel里面去

# 计算打卡的统计时间
now = datetime.datetime.now()     # 输入查卡日期，默认是今天
# now = datetime.date(2019,5,13)      # 输入查卡日期，自定义
time2 = datetime.timedelta(days=8)  # 统计一个星期的数据
day_now = str(now).split(" ")[0]
day_end = now - time2
day_end = str(day_end).split(" ")[0]

ID_total = input("请输入你的扇贝ID：")
print('\n')
#ID_total = "16888030"
ID_total = ID_total.split(",")   # 如果输入多个ID，用“，”分开
for ID in ID_total:
    web = "https://www.shanbay.com/api/v1/checkin/user/"+str(ID)+"/"
    shanbay = urlopen(web)    
    shanbay_data = shanbay.read().decode()
    
    # 获取昵称
    find_username = re.findall("username\".*?,",shanbay_data)[0]
    username = str(find_username)[len("username\": \""):-2]
    
    # 获取打卡数据
    find_data = re.findall("\"stats\".*?track_object_img" ,shanbay_data)
    find_start = "\"stats\": "
    find_end = "\"track_object_img\""

    num_today = "\"num_today\": "
    used_time = "\"used_time\": "

    # 初始化各项统计数据
    count = 0
    time_read = 0
    time_listen = 0
    time_bdc = 0
    time_sentence = 0
    count_read = 0
    count_listen = 0
    count_bdc = 0
    count_sentence = 0
    
    i = 1  #定义Excel表格的行数，从第二行开始写入，第一行已经写了表头

    # 获取打卡天数
    checkin_time = []
    num_checkin_days = []
    find_checkin = re.findall("\"checkin_time\".*?\"share_urls\"",shanbay_data) 
    for checkin in find_checkin:
        shanbey_time = checkin.split(",")[0]
        shanbey_days = checkin.split(",")[3]
        checkin_time.append(str(shanbey_time)[len("\"checkin_time\": \""):len("\"checkin_time\": \"")+10])
        num_checkin_days.append(str(shanbey_days)[len("\"num_checkin_days\": "):])
    
    print("上周打卡情况：")
    
    for data in find_data:       
        read = re.findall("\"read\":.*?}",data)
        if read == []:
           read = "{num_today\": 0, \"used_time\": 0.0}"
        
        listen = re.findall("\"listen\":.*?}",data)
        if listen == []:
            listen = "{num_today\": 0, \"used_time\": 0.0}"
        
        sentence = re.findall("\"sentence\":.*?}",data)
        if sentence == []:
            sentence = "{num_today\": 0, \"used_time\": 0.0}"
        
        bdc = re.findall("\"bdc\":.*?}",data)
        if bdc == []:
            bdc = "{num_today\": 0, \"used_time\": 0.0}"    
    
        read_num = re.findall(r"\d+\.?\d*",str(read))[0]
        read_time = re.findall(r"\d+\.?\d*",str(read))[1]
    
        listen_num = re.findall(r"\d+\.?\d*",str(listen))[0]
        listen_time = re.findall(r"\d+\.?\d*",str(listen))[1]
    
        bdc_num = re.findall(r"\d+\.?\d*",str(bdc))[0]
        bdc_time = re.findall(r"\d+\.?\d*",str(bdc))[1]
    
        sentence_num = re.findall(r"\d+\.?\d*",str(sentence))[0]
        sentence_time = re.findall(r"\d+\.?\d*",str(sentence))[1]     
        
        
        if checkin_time[count] >= day_now:
            count += 1
        elif checkin_time[count] > day_end:            
            # 统计总时间和各项时间
            time_total = float(read_time)+float(listen_time)+float(bdc_time)+float(sentence_time);
            time_read = time_read+float(read_time);
            time_listen = time_listen+float(listen_time);
            time_bdc = time_bdc+float(bdc_time);
            time_sentence = time_sentence+float(sentence_time);  
            
            # 统计各项数目累计
            count_read = count_read+float(read_num)
            count_listen = count_listen+float(listen_num)
            count_bdc = count_bdc+float(bdc_num)
            count_sentence = count_sentence+float(sentence_num) 
            
            # 输出一周每日打卡情况
            print("{},打卡{}天：阅读{}篇,听力{}句,单词{}个,炼句{}句,学习时间{}分钟".format(checkin_time[count],num_checkin_days[count],read_num,listen_num,bdc_num,sentence_num,time_total))
            count += 1
            
            # 把内容保存到Excel
            sheet.write(i, 0, checkin_time[count])  # 第i行，第1列
            sheet.write(i, 1, bdc_num)  # 第i行，第2列
            sheet.write(i, 2, read_num)  # 第i行，第3列
            sheet.write(i, 3, sentence_num)  # 第i行，第4列
            sheet.write(i, 4, listen_num)  # 第i行，第5列
            sheet.write(i, 5, time_total)  # 第i行，第6列
            i += 1

        else:
            break
        
print('\n')    
print("单词:{}分钟，总计{}个".format(time_bdc,count_bdc))
print("阅读:{}分钟，总计{}篇".format(time_read,count_read))
print("炼句:{}分钟，总计{}句".format(time_sentence,count_sentence))
print("听力:{}分钟，总计{}句".format(time_listen,count_listen))
print('\n') 
print("打卡时长:{}分钟".format(time_read+time_sentence+time_bdc+time_listen))
print('\n') 


# 保存Excel表
workbook.save('C:/Users/Administrator/Desktop/扇贝打卡.xls')
print('写入excel成功')
print("文件位置：")
print("C:/Users/Administrator/Desktop/扇贝打卡.xls")
print('\n') 
input("Please <Enter>")     