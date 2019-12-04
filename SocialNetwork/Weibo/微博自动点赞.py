ou# -*- coding: utf-8 -*-
"""
Created on Thu Oct 10 08:55:37 2019

@author: Administrator
"""

import requests

class WeiboSpider:
    def __init__(self, username, password):
        #  使用session保存登入状态
        self.session = requests.Session()
        # 头文件
        self.headers = {
                'Referer': "https://passport.weibo.cn/signin/login?entry=mweibo&res=wel&wm=3349&r=https://m.weibo.cn/compose/",
                'User-Agent': "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Mobile Safari/537.36"
                }
        self.session.headers.update(self.headers)
        self.username = username
        self.password = password

    def login(self):
        # 登入微博网址
        URL_login = "https://passport.weibo.cn/sso/login"  
        # 登入参数
        data_login = {
                'username': self.username,
                'password': self.password,
                'savestate': '1',
                'r': 'https://m.weibo.cn/compose/',
                'ec': '0',
                'pagerefer': 'https://m.weibo.cn/login?backURL=https%3A%2F%2Fm.weibo.cn%2Fcompose%2F',
                'entry': 'mweibo',
                'wentry': '',
                'loginfrom': '',
                'client_id': '',
                'code': '',
                'qq': '',
                'mainpageflag': '1',
                'hff': '',
                'hfp': ''
                }              
        self.session.post(URL_login, data=data_login)


    def get_st(self):
        # 获取st值
        URL_st = "https://m.weibo.cn/api/config"
        req_st = self.session.get(URL_st)
        config = req_st.json()
        st = config['data']['st']
        return st

    def compose(self,content):
        # 评论网址
        URL_comment = "https://m.weibo.cn/api/statuses/update"
        # 构造评论参数
        data_compose = {
          'content': content,
          'st': self.get_st()
        }
        
        # 实现评论功能
        req_compose = self.session.post(URL_comment, data=data_compose)
        print(req_compose.status_code)
        
    def send(self, content):
        self.login()
        self.compose(content)
        
    # 获取微博列表
    def get_weibo_list(self):
        params = {
                'uid': '2139359753',
                'luicode': '10000011',
                'lfid': '100103type=3&q=扇贝&t=0',
                'type': 'uid',
                'value': '2139359753',
                'containerid': '1076032139359753'
                }
        weibo_list_req = self.session.get('https://m.weibo.cn/api/container/getIndex', params=params)
        weibo_list_data = weibo_list_req.json()
        weibo_list = weibo_list_data['data']['cards']
        return weibo_list
        
    # 点赞微博
    def vote_up(self, id):
        vote_up_data = {
          'id': id,  # 要点赞的微博 id
          'attitude': 'heart',
          'st': self.get_st()
        }
        vote_up_req = self.session.post('https://m.weibo.cn/api/attitudes/create', data=vote_up_data)
        json = vote_up_req.json()
        print(json['msg'])
        
    # 批量点赞微博
    def vote_up_all(self):
        self.login()
        weibo_list = self.get_weibo_list()
        for i in weibo_list:
            # card_type 为 9 是正常微博
            if i['card_type'] == 9:
                self.vote_up(i['mblog']['id'])

username = input("请输入用户名：")
password = input("请输入密码：")
weibo = WeiboSpider(username, password)

# 自动发微博
# weibo.send('本条微博由 Python 自动发送')

# 自动点赞
weibo.vote_up_all()