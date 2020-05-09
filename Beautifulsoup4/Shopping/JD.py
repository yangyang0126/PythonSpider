# -*- coding: utf-8 -*-
"""
Created on Thu Oct 31 16:58:07 2019

@author: Administrator
"""

import requests
from bs4 import BeautifulSoup  # 解析网页数据

web_taobao = "https://search.jd.com/Search"

headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"
        }

params = {
        "keyword": "雅诗兰黛 眼霜",
        "enc": "utf-8",
        "wq": "雅诗兰黛 眼霜",
        "pvid": "11f25f6b9dca4de2865702db69b06bf9"
        }

res = requests.get(web_taobao, headers=headers, params=params)
soup = BeautifulSoup(res.text, 'html.parser')
items = soup.find_all("li", class_="gl-item") 
for i in range(10):
    item = items[i]
    productPrice = item.find("div", class_="p-price").text.strip()
    try:
        productTitle = item.find("div", class_="p-name p-name-type-2").text.strip()
    except:
        productTitle = item.find("div", class_="productTitle productTitle-spu").text.strip()
    productShop = item.find("div", class_="productShop").text.strip()
    try:
        productStatus = item.find("p", class_="productStatus").text.strip()
    except:
        productStatus = "暂无成交数据"
    print(productTitle,productPrice,productStatus,productShop)
    print("\n")
