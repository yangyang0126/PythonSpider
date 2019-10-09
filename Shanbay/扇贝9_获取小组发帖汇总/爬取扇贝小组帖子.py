# -*- coding: utf-8 -*-
"""
Created on Sat Jun  8 20:00:41 2019

@author: YangYang
"""


import requests
import json
import re
import xlwt
  



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
account =input("请输入你的账号：")
password = input("请输入你的密码：")

s,r = Login(account,password)
print('\n') 
print("账号登入成功！")



# 打开Excel
workbook = xlwt.Workbook()  #定义workbook
sheet = workbook.add_sheet('社区')  #添加sheet
head = [ '标题','链接','作者']
for h in range(len(head)):
    sheet.write(0, h, head[h])    #把表头写到Excel里面去

print('\n') 
print("Excel汇总表已创建")
print('\n') 

i = 1
j = 1
k = 1

# 默认爬取5页
for page in range(1,5):    
    print("正在取读第{}数据".format(page))
    web = 'https://www.shanbay.com/api/v1/team/44584/thread/?page='+str(page)
    Text_article = GetTextWeb(web,s)
    
    # 提取标题
    e_title = []
    list_title = re.findall("(\"title\": \".*?\"),",Text_article)

    for title in list_title:
        #title = list_title[1]
        title = "{"+title+"}"  #转成字典     
        title_dict = json.loads(title)
        #title_dict = json.loads(title)
        # e_title.append(title_dict['title'])
        if not (title_dict['title'] == "再次出发的30岁"):
            sheet.write(i, 0, "["+title_dict['title']+"]")
            i += 1
        
    #  提取作者
    e_nickname = []
    list_nickname = re.findall("(\"nickname.*?),",Text_article)

    for nickname in list_nickname: 
        nickname = "{"+nickname+"}"  #转成字典
        nickname_dict = json.loads(nickname)
        # e_nickname.append(nickname_dict['nickname'])  
        sheet.write(j, 2, nickname_dict['nickname'])
        j += 1
    
 
    #  提取网址      
    e_share_url = []
    list_share_url = re.findall("(\"share_url\".*?),",Text_article)

    for share_url in list_share_url: 
        share_url = "{"+share_url+"}"  #转成字典
        share_url_dict = json.loads(share_url)
        # e_share_url.append(share_url_dict['share_url'])  
        sheet.write(k, 1, "("+share_url_dict['share_url']+")")
        k += 1
        
        
    
workbook.save("扇贝小组发帖汇总.xls")
print('\n') 
print('写入excel成功')
print("文件位置：和代码在同一个文件夹")
print('\n') 
#input("取读完毕，点击回车退出")