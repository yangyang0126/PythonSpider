# -*- coding: utf-8 -*-
"""
Created on Sat May 25 2019

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

# 输入网址
sentence_number = 40
book_url = "https://www.shanbay.com/api/v1/sentence/userbook/" + str(sentence_number)
book_phrase_url = "https://www.shanbay.com/api/v1/sentence/book/phrase/"+ str(sentence_number)
book_article_url = "https://www.shanbay.com/api/v1/sentence/book/article/"+ str(sentence_number)

# 获取炼句书的标题
#Text_book = GetTextWeb(book_url,s)
#title = re.findall("(\"title\".*?),",Text_book)
#title = "{"+title[0]+"}"  #转成字典
#title_dict = json.loads(title)
#workbook_title =  title_dict['title']+".xls"  # 给Excel表格命名
workbook_title =  "六级阅读短语训练.xls"  # 给Excel表格命名
print('\n') 
print("正在取读炼句数据，请等待……")
# 获取炼句
Text_article = GetTextWeb(book_article_url,s)
article_List = re.findall("{\"status.*?}",Text_article)

sheet = workbook.add_sheet('课程内容')  #添加sheet
head = [ '内容', '解释']
for h in range(len(head)):
    sheet.write(0, h, head[h])    #把表头写到Excel里面去
m = 1 #Excel开始写入的位置  
n = 1 #Excel开始写入的位置  
for article in article_List:
    article_dict = json.loads(article)
    article_id = article_dict['article_id']
    article_id_url = book_article_url+"/"+str(article_id)
    Text_article_id = GetTextWeb(article_id_url,s)
    
    content_article_1 = re.findall(" {\"zh-CN\": {\"content.*?}",Text_article_id)
    for content1 in content_article_1:        
        content1 = content1[len("{\"zh-CN\":")+2:]
        content_dict_1 = json.loads(content1)
        sheet.write(m, 1, content_dict_1['content'])
        m += 1
        
    content_article_2 = re.findall("(\"audio_name.*?), \"audio_urls",Text_article_id)    
    if content_article_2 == []:
        content_article_2 = re.findall("(\"content\".*?\"),",Text_article_id)
        for i in content_article_2:
            if i[len("\"content\": \"")] == "\\":
                 content_article_2.remove(i)
        for i in content_article_2:
            if i[len("\"content\": \"")] == "\\":
                 content_article_2.remove(i)
    for content2 in content_article_2:
        content2 = "{"+content2+"}"  #转成字典
        content_dict_2 = json.loads(content2)
        sheet.write(n, 0, content_dict_2['content'])    
        n += 1
        
print('\n') 
print("正在取读单词和短语数据，请等待……")        
# 获取单词和短语
Text_phrase = GetTextWeb(book_phrase_url,s)
phrase_List = re.findall("{\"content.*?}",Text_phrase)

sheet = workbook.add_sheet('单词和短语')  #添加sheet
head = [ '内容', '解释']
for h in range(len(head)):
    sheet.write(0, h, head[h])    #把表头写到Excel里面去
j = 1 #Excel开始写入的位置  

for phrase in phrase_List:
    phrase_dict = json.loads(phrase)
    sheet.write(j, 0, phrase_dict['content'])
    sheet.write(j, 1, phrase_dict['definition'])
    j += 1

  
workbook.save(workbook_title)
print('\n') 
print('写入excel成功')
print("文件位置：和代码在同一个文件夹")
print('\n') 
input("炼句取读完毕，点击回车退出")
