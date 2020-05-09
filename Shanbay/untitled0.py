# -*- coding: utf-8 -*-
"""
Created on Fri Apr 10 09:06:26 2020
@author: Yenny
"""

import requests  # 获取网页数据
ID = "16888030"
web = "https://www.shanbay.com/api/v1/checkin/user/"+str(ID)+"/"  # 网址：打卡记录
res = requests.get(web)  # requests发起请求，静态网页用get
LearningData = res.json()

NickName = LearningData['data'][0]['user']['nickname']  # 获取昵称

for LearningDataDaily in LearningData['data']:
    checkin_date =  LearningDataDaily['checkin_date']
    try:
        bdc_num_today = LearningDataDaily['stats']['bdc']['num_today']
        bdc_used_time = LearningDataDaily['stats']['bdc']['used_time']        
    except:  
        bdc_num_today = 0
        bdc_used_time = 0.0        
    print("{}，{}背单词{}个，用时{}分钟".format(checkin_date,NickName,bdc_num_today,bdc_used_time))