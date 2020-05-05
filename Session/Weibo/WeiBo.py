ou# -*- coding: utf-8 -*-
"""
Created on Thu Oct 10 08:55:37 2019

@author: Administrator
"""

import requests

# 登入微博
def Login(username,password):
    RequestURL = "https://passport.weibo.cn/sso/login"   
    RequestHeaders = {
            'Referer': "https://passport.weibo.cn/signin/login?entry=mweibo&res=wel&wm=3349&r=https://m.weibo.cn/compose/",
            'User-Agent': "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Mobile Safari/537.36"
            }    
    FormData = {
            'username': username,
            'password': password,
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
    LoginSession = requests.Session()
    LoginSession.headers.update(RequestHeaders)
    Res = LoginSession.post(RequestURL, data=FormData)
    if Res.status_code == 200:
        print("登入成功")
    else:
        print("登入失败")
    return LoginSession

# 获取st
def GetST(LoginSession):
    RequestConfig = LoginSession.get('https://m.weibo.cn/api/config')
    Config = RequestConfig.json()
    st = Config['data']['st']
    return st

# 发微博
def SendContent(LoginSession,content):   
    st = GetST(LoginSession)
    DataCompose = {
      'content': content,
      'st': st
    }
    ResCompose = LoginSession.post('https://m.weibo.cn/api/statuses/update', data=DataCompose)
    if ResCompose.status_code == 200:
        print("发表微博成功")
    else:
        print("发表微博失败")
    return ResCompose

# 获取微博列表
def GetList(LoginSession):
    URL = 'https://m.weibo.cn/api/container/getIndex'
    DataList = {            
            'uid': '2139359753',
            't': '0',
            'luicode': '10000011',
            'lfid': '100103type=1&q=扇贝网',
            'type': 'uid',
            'value': '2139359753',
            'containerid': '1076032139359753'
            }
    WeiBoListReq = LoginSession.get(URL, params=DataList)
    WeiBoListData = WeiBoListReq.json()
    WeiBoList = WeiBoListData['data']['cards']
    return WeiBoList

# 点赞
def SendHeart(LoginSession,ID):
    st = GetST(LoginSession)
    DataHeart = {
            'id': ID,
            'attitude': 'heart',
            'st': st
            }
    ResHeart = LoginSession.post('https://m.weibo.cn/api/attitudes/create', data=DataHeart)
    if ResHeart.status_code == 200:
        print("点赞成功")
    else:
        print("点赞失败")    
    return ResHeart

# 批量点赞
def SendHeartAll(LoginSession):
    WeiBoList = GetList(LoginSession)
    for i in WeiBoList:
        # card_type=9的时候，是一个正常的微博
        if i['card_type'] == 9:
            SendHeart(LoginSession,i['mblog']['id'])

# 发表评论
def SendComment(LoginSession,Comment,ID):
    st = GetST(LoginSession)
    DataComment = {
            'content': Comment,
            'mid': ID,
            'st': st
            }
    ResComment = LoginSession.post('https://m.weibo.cn/api/comments/create', data=DataComment)
    if ResComment.status_code == 200:
        print("评论成功")
    else:
        print("评论失败")    
    return ResComment

# 批量评论
def SendCommentAll(LoginSession,Comment): 
    WeiBoList = GetList(LoginSession)
    for i in WeiBoList:
        # card_type=9的时候，是一个正常的微博
        if i['card_type'] == 9:
            SendComment(LoginSession,Comment,i['mblog']['id'])
           
LoginSession = Login("用户名","密码")
SendContent(LoginSession,"本条微博由Python发送")
SendHeartAll(LoginSession)
Comment = "给扇贝Python课程点赞，此留言由Python自动发送"
SendCommentAll(LoginSession,Comment)


