# -*- coding: utf-8 -*-
"""
Created on Wed May 13 14:24:27 2020
@author: Yenny
"""

from selenium import webdriver
import  time


browser = webdriver.Chrome()
# 打开博客
browser.get('https://sh.58.com/?utm_source=market&spm=u-2d2yxv86y3v43nkddh1.BDPCPZ_BT')
time.sleep(0.3)