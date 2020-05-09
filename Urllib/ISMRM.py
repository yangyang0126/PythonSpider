# -*- coding: utf-8 -*-
"""
Created on Wed May 15 2019

@author: Administrator
"""
from urllib.request import urlopen
import re
import os
import xlwt

print("开始读取目录，文件位置：")
print("F:/ISMRM2018small/ISMRM2018small/cds.ismrm.org/protected/18MPresentations/abstracts/")
print('\n')
print("正在读取……")

# 所在文件夹位置
input_dir = 'F:/ISMRM2018small/ISMRM2018small/cds.ismrm.org/protected/18MPresentations/abstracts/'
file_name = os.listdir(input_dir) #列出文件夹下所有的目录与文件

count = 0
title = [0 for num in range(6000)] # 初始化数组大小
Auther = [0 for num in range(6000)] 
number = [0 for num in range(6000)] 

for file_need in file_name:  
    if re.search("html$",file_need):    
        location = "file:///"+str(input_dir)+str(file_need)
        ISMRM = urlopen(location) 
        ISMRM_data = ISMRM.read().decode()

         # 获取标题
        find_title = re.findall("\"submissionTitle\">.*?<",ISMRM_data)
        title[count] = str(find_title)[len("\"submissionTitle\">")+2:-3]

        # 获取作者
        find_Auther = re.findall("'affAuthers\'>.*?<",ISMRM_data)
        Auther[count] = str(find_Auther)[len("\'affAuthers\'>")+2:-3]

        # 获取序号
        number[count] = str(file_need)[:-5]

        count += 1        
        #data_output.writelines(num)
        #print(num,title,Auther,file = data_output)      
        
    else:
        continue
            

def save_to_excel(number,title,Auther,count):
    try:
        workbook = xlwt.Workbook()
        sheet = workbook.add_sheet('ISMRM2018')
        head = ['序号', '标题', '作者']    #表头
        for h in range(len(head)):
            sheet.write(0, h, head[h])


        for i in range(count):
            sheet.write(i+1, 0, number[i])
            sheet.write(i+1, 1, title[i])
            sheet.write(i+1, 2, Auther[i])

           
        workbook.save('C:/Users/Administrator/Desktop/ISMRM2018.xls')
        print('写入excel成功')
        print("文件位置：")
        print("C:/Users/Administrator/Desktop/ISMRM2018.xls")
    except Exception:
        print('写入excel失败')
        
save_to_excel(number,title,Auther,count)

print('\n')
input("目录读取完毕，点击任意键退出")
            