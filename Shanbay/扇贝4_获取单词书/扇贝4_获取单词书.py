# -*- coding: utf-8 -*-
"""
Created on Fri May 24 2019

@author: YangYang
"""

'''
web_shanbay：扇贝网址
web_number：单词书编号
web_wordbook：单词书网址
web_wordlist：单词书——Unit网址
web_wordpage：单词书——Unit——分页网址

web_wordbook_data：单词书网页数据
web_wordlist_data：Unit网页数据
web_wordpage_data：Unit分页网页数据

wordlist_name：Unit名称
wordlist_id：Unit编号

'''

from urllib.request import urlopen
import re
import xlwt
import math


# 获取单词书网页数据
def FindWordbookData(web_number):    
    web_shanbay = "https://www.shanbay.com/wordbook/"
    web_wordbook = web_shanbay + str(web_number) + "/"
    web_wordbook = urlopen(web_wordbook)
    web_wordbook_data = web_wordbook.read().decode()
    return web_wordbook_data

# 定位该单词书所有的Unit和对应网址
def FindWebWordlist(web_number,web_wordbook_data): 
    find_address = "<a href=\"/wordlist/" + str(web_number) + ".*?</a>"
    find_wordlist = re.findall(find_address,web_wordbook_data) 
    # 获取Unit和网址
    wordlist_id = []
    wordlist_name = []
    web_wordlist = []
    for wordlist in find_wordlist:
        ID = wordlist.split('/')[3]
        name = wordlist.split('>')[1]
        name = name[:-3]
        wordlist_name.append(name)
        wordlist_id.append(ID)
        web_wordlist.append("https://www.shanbay.com/wordlist/" + str(web_number) + "/" + str(ID) + "/")
    return web_wordlist

# 获取网页取读数据
def ReadWebData(web):    
    web_read = urlopen(web)
    web_read = web_read.read().decode()
    return web_read

# 获取页数
def CalPage(web_data):
    wordlist_num_vocab = re.findall("var pages = Math.ceil(.*?)/",web_data)
    wordlist_num_vocab = str(wordlist_num_vocab[0])[1:]
    var_pages = math.ceil(float(wordlist_num_vocab)/20)
    return var_pages

# 获取标题
def FindTitle(web_data):
    web_title = re.findall("<title>单词书： (.*?) </title>",web_data)
    return web_title


a = '''
部分单词书编号：
TOEFL核心词汇21天突破:202
扇贝托业词汇精选:91918
扇贝循环单词书·六级（乱序）:197656
高中标准词汇表:16
人教版小学一年级上:204316
'''
print(a)
web_number = input("请输入单词书编号:")
#web_number = 202 #这里需要根据你想爬取的单词书，需要改
web_wordbook_data = FindWordbookData(web_number)    
web_wordlist = FindWebWordlist(web_number,web_wordbook_data)
print('\n')
print("正在取读数据，请等待……")

# 定义保存Excel的位置
workbook = xlwt.Workbook()  #定义workbook    


for wordlist in web_wordlist:    
    web_wordlist_data = ReadWebData(wordlist)
    
    # 打开Excel，保存Sheet和表头
    title = re.findall("<title>词串：  (.*?) </title>",web_wordlist_data)
    sheet = workbook.add_sheet(str(title[0]))  #添加sheet  
    head = ['单词', '解释']    #表头
    for h in range(len(head)):
       sheet.write(0, h, head[h])    #把表头写到Excel里面去
    m = 1 #定义Excel的行数    
    
    # 获取Unit的页码和相应内容
    var_pages = CalPage(web_wordlist_data)
    for i in range(1,var_pages+1):
        web_wordpage = str(wordlist) + "?page=" + str(i)    
        web_wordpage_data = ReadWebData(web_wordpage)
    
        # 开始获取单词和解释
        find_word = re.findall("<strong>([a-z,A-Z]*?)</strong>",web_wordpage_data) 
        find_meaning = re.findall("<td class=\"span10\">(.*?)</td>",web_wordpage_data,re.S) 
        find_result = zip(find_word,find_meaning) 
        for word,meaning in find_result:            
            sheet.write(m, 0, word)
            sheet.write(m, 1, meaning)
            m += 1            

SaveAddress = FindTitle(web_wordbook_data)
SaveAddress = str(SaveAddress[0]) + ".xls"
workbook.save(SaveAddress)
print('\n') 
print('写入excel成功')
print("文件位置：和你的代码在一个文件夹下面")
print('\n') 
input("取读完毕，点击回车退出") 