# -*- coding: utf-8 -*-
"""
Created on Wed Sep  2 11:00:07 2020

@author: zhaoy
"""

#%%
import requests
import json
import re
import xlwt
  



def login(account,password):
    headersLogin = {"user-agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
                     "referer": "https://web.shanbay.com/web/account/login/",
                     "content-type": "application/json",
                     "accept-encoding": "gzip, deflate, br"
                     }

    linkLogin = "https://apiv3.shanbay.com/bayuser/login"
    s = requests.Session()  # 为了保存登入信息

    dataPayLoad  = {
                     'account': account,
                     'code_2fa': "",
                     'password': password     
                    }
    r = s.post(linkLogin, data=dataPayLoad, headers=headersLogin)
    return s,r

# 输入账号密码登入  
account = "13609290600"
password = "123456"

s,r = login(account,password)
if r.status_code == 200:
    print("账号登入成功！")
else:
    print("账号登入失败！")

#%%
s = requests.Session()
headerRequiredAccount = {"user-agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
                 "referer": "https://web.shanbay.com/web/account/login/",
                 "content-type": "application/json"
                
                 }
linkRequiredAccount = "https://apiv3.shanbay.com/bayuser/2fa/required?account=13609290600"   
reqRequiredAccount = s.get(linkRequiredAccount, headers=headerRequiredAccount)
print(reqRequiredAccount)
#%%
payLoadHeader = {"user-agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
                     "referer": "https://web.shanbay.com/web/account/login/",
                     "content-type": "application/json",
               
                   
                     }
postUrl = "https://apiv3.shanbay.com/bayuser/login"
payLoadData  = {
                 'account': account,
                 'code_2fa': "",
                 'password': password     
                }
r = s.post(postUrl, data=payLoadData, headers=payLoadHeader)
print(r)
#%%
linkTeam = "https://apiv3.shanbay.com/team/group/manage/members?ipp=10&page=1&rank_type=CHECKIN_RATE&order=POSITIVE"
paramsTeam = {
        "ipp": "10",
        "page": "1",
        "rank_type": "CHECKIN_RATE",
        "order": "POSITIVE"
        }
reqTeam = s.get(linkTeam, params=paramsTeam)