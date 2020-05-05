# -*- coding: utf-8 -*-
"""
Created on Wed Oct  9 14:28:18 2019

@author: Administrator
"""

import requests
import time
import xlwt  

headers = {
  'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
}
lasthotcommentid = ''
params = {
        'g_tk_new_20200303': '5381',
        'g_tk': '5381',
        'loginUin': '0',
        'hostUin': '0',
        'format': 'json',
        'inCharset': 'utf8',
        'outCharset': 'GB2312',
        'notice': '0',
        'platform': 'yqq.json',
        'needNewCode': '0',
        'cid': '205360772',
        'reqtype': '2',
        'biztype': '1',
        'topid': '1406731',
        'cmd': '8',
        'needmusiccrit': '0',
        'pagenum': 0,
        'pagesize': '25',
        'lasthotcommentid': lasthotcommentid,
        'domain': 'qq.com',
        'ct': '24',
        'cv': '10101010'
        }

def GetComment(headers, params):
    res = requests.get('https://c.y.qq.com/base/fcgi-bin/fcg_global_comment_h5.fcg', headers=headers, params=params)
    data = res.json()
    return data

workbook = xlwt.Workbook()     
row = 1
for pagenum in range(5):    
    params['pagenum'] = pagenum
    params['lasthotcommentid'] = lasthotcommentid
    data = GetComment(headers, params)
    print('爬虫QQ音乐：{}第{}页'.format(data['topic_name'],pagenum+1))    
    if pagenum == 0:        
        sheet = workbook.add_sheet(data['topic_name'])  
        head = ['昵称', '评价'] 
        for h in range(len(head)):
            sheet.write(0, h, head[h])            
    for item in data['comment']['commentlist']:
        sheet.write(row, 0, item['nick'])
        sheet.write(row, 1, item['rootcommentcontent'])    
        row += 1
    lasthotcommentid = data['comment']['commentlist'][-1]['commentid']
    time.sleep(1)
    
workbook.save('QQ音乐评论.xls')  
print('写入excel成功')