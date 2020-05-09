# -*- coding: utf-8 -*-
"""
Created on Fri Oct 25 15:02:24 2019

@author: Administrator
"""

import requests
from concurrent import futures
from bs4 import BeautifulSoup

session = requests.Session()
executor = futures.ThreadPoolExecutor(max_workers=5)

# 解析列表页，得到内容页链接
def parse_list_page(text):
  soup = BeautifulSoup(text, 'html.parser')
  ul = soup.find('div', class_='show-list').find('ul')
  urls = []
  prefix = 'https://bbs.hupu.com'
  for li in ul.find_all('li'):
    url = li.div.find('a', class_='truetit').attrs['href']
    url = prefix + url
    urls.append(url)
  return urls

# 解析内容页，得到标题和回复
def parse_content_page(text):
  soup = BeautifulSoup(text, 'html.parser')
  title = soup.find('h1', id='j_data').text
  
  contents = []
  for floor in soup.find_all('div', class_='floor'):
    floor_box = floor.find('div', class_='floor_box')
    if not floor_box:
      return None, None
    content = floor_box.table.tbody.tr.td.text
    contents.append(content)
  return title, contents

# 爬取列表页，解析出这一页的内容链接
def get_content_urls(list_url):
  res = session.get(list_url)
  content_urls = parse_list_page(res.text)
  return content_urls

# 爬取内容页，解析出标题和回复
def get_content(content_url):
  res = session.get(content_url)
  title, contents = parse_content_page(res.text)
  return title, contents

# 获取内容页链接
fs = []
url = 'https://bbs.hupu.com/acg'
fs.append(executor.submit(get_content_urls, url))
futures.wait(fs)
content_urls = set()
for f in fs:
  for url in f.result():
    content_urls.add(url)

# 爬取内容页
fs = []
for url in content_urls:
  fs.append(executor.submit(get_content, url))
futures.wait(fs)
result = {}
for f in fs:
  title, contents = f.result()
  if title:
    result[title] = contents

print(result.keys())
