# -*- coding: utf-8 -*-
"""
Created on Thu Oct 31 15:32:33 2019

@author: Administrator
"""

import requests
from bs4 import BeautifulSoup  # 解析网页数据

web_taobao = "https://list.tmall.com/search_product.htm"

headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"
        }

params = {
        "q": "雅诗兰黛 眼霜",
        "type": "p",
        "spm": "a220m.1000858.a2227oh.d100",
        "from": ".list.pc_1_searchbutton"
        }

res = requests.get(web_taobao, headers=headers, params=params)
soup = BeautifulSoup(res.text, 'html.parser')
items = soup.find_all("div", class_="product") 
for i in range(10):
    item = items[i]
    productPrice = item.find("p", class_="productPrice").text.strip()
    try:
        productTitle = item.find("p", class_="productTitle").text.strip()
    except:
        productTitle = item.find("div", class_="productTitle productTitle-spu").text.strip()
    productShop = item.find("div", class_="productShop").text.strip()
    try:
        productStatus = item.find("p", class_="productStatus").text.strip()
    except:
        productStatus = "暂无成交数据"
    print(productTitle,productPrice,productStatus,productShop)
    print("\n")
