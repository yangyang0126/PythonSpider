# -*- coding: utf-8 -*-
"""
Created on Tue Oct 29 16:46:28 2019

@author: Administrator
"""

import requests
import json
from bs4 import BeautifulSoup  # 解析网页数据
import datetime
import re

def Login(account,password):
    payloadHeader = {'user-agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
                     'referer': "https://web.shanbay.com/web/account/login/",
                     'content-type': 'application/json'
                     }

    postUrl = 'https://apiv3.shanbay.com/bayuser/login'
    s = requests.Session()  # 为了保存登入信息

    PayloadData  = {
                     'account': account,
                     'code_2fa': "",
                     'password': password     
                    }
    r = s.post(postUrl, data=json.dumps(PayloadData), headers=payloadHeader)
    return s,r

def GetTextWeb(url,s):
    GetUrl = s.get(url)
    return GetUrl.text

def GetDetails(href):
    url_checkin = "https://www.shanbay.com/api/v1"+href
    res = s.get(url_checkin)
    checkin_data = res.json()
    data_info = "未能获取学习记录"
    used_time = 0
    for data in checkin_data['data']:
        if data['checkin_date'] == str(now):            
            data_info = data['info']
            try:
                used_time = int(re.findall("学习时间(.*?)分钟",data_info)[0]) 
            except:                
                used_time = 0               
            return data_info, used_time
            

#计算打卡的统计时间
now = datetime.date.today()-datetime.timedelta(days=1)  
print("查卡日期：",now)
print('\n')

# 输入账号密码登入  
account = "13609290600"
password = "123456"  
s,r = Login(account,password)
print('\n') 
print("账号登入成功！")



url_member = "https://www.shanbay.com/team/manage/?page="
nicknames = []
points = []
days = []
rate = []
href = []
info_all = []
used_time = []
for page in range(1,48):
    print("正在取读第{}页数据".format(page))
    params_member = {
            "page": page
            }
    res = s.get(url_member, params=params_member)
    soup = BeautifulSoup(res.text, 'html.parser')
    items = soup.find_all("tr", class_="member") 
    for item in items:
        nicknames.append(item.find("a", class_="nickname").text) # 用户
        points.append(item.find("td", class_="points").text.strip())# 贡献成长值
        days.append(item.find("td", class_="days").text.strip()) # 组龄
        rate.append(item.find("td", class_="rate").text.strip()) # 打卡率
        href.append(item.find("a", class_="nickname")["href"])
        checked = item.find("td", class_="checked").text.strip()
        info = "昨日未打卡"
        time = 0
        if checked == "已打卡":
            [info, time] = GetDetails(item.find("a", class_="nickname")["href"])
        info_all.append(info)    
        used_time.append(time)    

TxtTitle = "打卡排行"+str(now)+".txt"
f = open(TxtTitle,'a')        
for m in range(10): 
    i = used_time.index(max(used_time))
    f.write("- [{}](https://www.shanbay.com{})，{}".format(nicknames[i],href[i],info_all[i]))        
    f.write('\n')
    f.write('\n')
    del nicknames[i]
    del points[i]
    del days[i]
    del rate[i]
    del info_all[i]
    del used_time[i]
    del href[i]
f.close() 

       

    
        






