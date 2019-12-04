# -*- coding: utf-8 -*-
"""
Created on Wed Oct 30 17:21:22 2019

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


# 输入账号密码登入  
account = "13609290600"
password = "123456"  
s,r = Login(account,password)
print('\n') 
print("账号登入成功！")


url_topic = "https://www.shanbay.com/api/v1/forum/45376/thread/"

headers = {
        "referer": "https://www.shanbay.com/team/detail/44584/",
        "user-agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"
}

data_compose = {            
            "csrfmiddlewaretoken": "BfrBEAMD5Y0edgX58T4az8egXIrFoqO4",
            "title": "机器人测试",
            "body": "代码测试，请忽略"
            }
res = s.post(url_topic, headers=headers, data=data_compose)
print(res.status_code)
