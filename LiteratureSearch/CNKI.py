# -*- coding: utf-8 -*-
"""
Created on Fri Nov  8 16:57:40 2019

@author: Administrator
"""

from selenium import webdriver
import  time

browser = webdriver.Chrome()
# 打开博客
browser.get('http://wap.cnki.net/touch/web/guide')
time.sleep(0.3)
# 输入主题
browser.find_element_by_id('txt_1_value1').send_keys('地下空间')
browser.find_element_by_class_name('c7').click()
time.sleep(0.3)
# 输入来源类别
browser.find_element_by_id('mediaBox4').click()
time.sleep(0.3)
# 设置文献分类目录
browser.find_element_by_css_selector("input[value=\"清除\"]").click()
browser.find_element_by_id('Gfirst').click()
browser.find_element_by_name("法理、法史").click()
browser.find_element_by_name("宪法").click()
browser.find_element_by_name("行政法及地方法制").click()
browser.find_element_by_name("民商法").click()
browser.find_element_by_name("刑法").click()
browser.find_element_by_name("经济法").click()
browser.find_element_by_name("诉讼法与司法制度").click()
browser.find_element_by_name("国际法").click()
# 搜索
browser.find_element_by_id('btnSearch').click()
# 查找文献
titles = browser.find_element_by_css_selector("a[class=\"fz14\"]")









# 找到登录按钮
login_btn = browser.find_element_by_link_text('登录')
# 点击登录按钮
login_btn.click()
# 找到用户名输入框
user_login = browser.find_element_by_id('user_login')
# 输入用户名
user_login.send_keys('codetime')
# 找到密码输入框
user_pass = browser.find_element_by_id('user_pass')
# 输入密码
user_pass.send_keys('shanbay520')
# 找到登录按钮
wp_submit = browser.find_element_by_id('wp-submit')
# 点击登录按钮
wp_submit.click()
# 找到第一篇文章
more_link = browser.find_element_by_class_name('more-link')
# 点击第一篇文章
more_link.click()
# 找到评论框
comment = browser.find_element_by_id('comment')
# 输入评论
comment.send_keys('由 selenium 自动评论')
# 找到发表评论按钮
submit = browser.find_element_by_id('submit')
# 点击发表评论按钮
submit.click()
# 关闭浏览器
browser.quit()