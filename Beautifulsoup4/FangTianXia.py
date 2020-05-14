# -*- coding: utf-8 -*-
"""
Created on Thu May 14 12:30:19 2020
@author: Yenny
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 17:55:00 2020

@author: dingdong
"""


import requests
from bs4 import BeautifulSoup
import xlwt
import time

row = 1
workbook = xlwt.Workbook(encoding = 'utf-8')
sheet = workbook.add_sheet('房天下广州')
head = ['项目','地段','价格','物业类型','年限','开盘时间','开发商','开盘动态','详情链接']
for h in range(len(head)):
    sheet.write(0,h,head[h])
    
for number in range(1): # 10页
    url = 'https://gz.newhouse.fang.com/house/s/b1saledate-b9'+str(number+1)+'/'
    headers = {
              'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
            }
    res = requests.get(url,headers=headers)
    res.encoding = "gbk" 
    soup = BeautifulSoup(res.text,'html.parser')
    content = soup.find('div',class_='contentListf fl clearfix')
    items = content.find_all('li',{'id':True}) 

    for item in items:
        #获取列表页面信息
        try:
            ref = 'https:'+str(item.select('div.nlcd_name a')[0]['href']) #详情链接
        except:
            continue
        id_= item['id'].strip('lp_')
        location = item.select('div.address a')[0].text.strip()#地段
        price = item.select('div.nhouse_price')[0].text.strip()#价格
        project = item.select('div.nlcd_name')[0].text.strip()
        detail = ref+'house/'+id_+'/housedetail.htm'
        dongtai = ref+'house/'+id_+'/dongtai.htm'
       
        #获取详情页面信息
        res1 = requests.get(detail,headers=headers)
        res1.encoding = "gbk"  
        soup1 = BeautifulSoup(res1.text,'html.parser')       
     
        try:
            type_ = soup1.find_all('div',class_='list-right')[0].text.strip()#物业类型
        except:
            continue
        year = soup1.find_all('div',class_='list-right')[4].text.strip()#年限
        openning = soup1.find_all('div',class_='list-right')[7].text.strip()#开盘时间
        builder = soup1.select('div.list-right-text')[0].text#开发商

        #获取动态页面信息
        res2 = requests.get(dongtai,headers=headers)
        res2.encoding = "gbk"   
        soup2 = BeautifulSoup(res2.text,'html.parser')
        storylists = []
        a = soup2.select('li.storyList')
        
        sheet.write(row,0,project)
        sheet.write(row,1,location)
        sheet.write(row,2,price)
        sheet.write(row,3,type_)
        sheet.write(row,4,year)
        sheet.write(row,5,openning)
        sheet.write(row,6,builder)
        sheet.write(row,8,ref)
        
        for i in range(len(a)):
            storylist = soup2.select('li.storyList')[i].text.replace('\n','').strip()
            storylists.append(storylist)
        story = '-'.join(storylists)#开盘动态
        sheet.write(row,7,story)
        row += 1
    print('===============第{}页爬取完毕==============='.format(number+1))
    time.sleep(1)
workbook.save('房天下房源信息.xls')  # 和代码在一个路径下
print('写入excel成功')

    