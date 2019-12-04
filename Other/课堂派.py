# -*- coding: utf-8 -*-
"""
Created on Mon Nov 11 09:50:42 2019

@author: Administrator
"""

import requests

headers = {
    "origin": "https://w.ketangpai.com",
    "referer": "https://w.ketangpai.com/pages/data/data.html",
    "user-agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"

}
params = {
    "courseid": "MDAwMDAwMDAwMLOsx9yIqatp",
    "token": "MDAwMDAwMDAwMMurrpWavLehhs1-lLGpeZKFt4OUepuomcWmmqaMiHtnr5ylzYWosKKZq6HQxtOK0ZCme5p6nHaZrnyrnZWiiJnKebqUmryXpIDOpNyyuZvbhKd_loB2dmPIip5w"
}
res = requests.get('https://openapi.ketangpai.com/CoursewareApi/listAll', headers=headers, params=params)
data = res.json()["lists"]
for list_data in data:    
    name = list_data["name"]
    rurl = list_data["rurl"]
    print(name)


    
wb =  requests.get("https://document.ketangpai.com/img/?img=8BTy2gSXw1KDYtd15jGeNTBw1RFDIfNpAH8ZqYezcMewei7qAzMzR2PWnfr7UnokPLSX5p4KeEI=&tp=")   
content = wb.content #获取页面内容
fp = open("test.jpg","ab") #打开一个文本文件
fp.write(content) #写入数据
fp.close() #关闭文件