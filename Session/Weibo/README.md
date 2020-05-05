# 爬虫：新浪微博发表、评论、点赞

- **GET** 用于获取数据，比如刷微博，用`params`
- **POST** 用于提交数据，比如登录微博，用`data`

## 微博登入

打开微博客户端：[https://m.weibo.cn/](https://m.weibo.cn/)，右击打开”检查“（有的浏览器叫”审查元素“）

![](http://cdn.zhaojingyi0126.com/IMG/17569167-d920ef8e065f1812.png)


点上图的小图标，可以切换网页版和手机版，手机版相对好爬一点

点击`Preserve log`，保留登入信息，接着输入账号密码登入

![](http://cdn.zhaojingyi0126.com/IMG/17569167-5f986eb6e1f3ed5f.png)

关注左侧`login`，这里面就是我们要爬取的信息

### 获取登入网址

![](http://cdn.zhaojingyi0126.com/IMG/17569167-adc41d9c38befedb.png)

```
URL_login = "https://passport.weibo.cn/sso/login"
```

### 获取头文件

一般 **referer**（请求来源页面）、**origin**（谁发起的请求）、**host**（主机名及端口号） 字段也常被用于反爬虫，当我们的爬虫无法正常获取数据时，我们可以将请求头里的这些字段照搬进去试试。

![](http://cdn.zhaojingyi0126.com/IMG/17569167-ea423d2029e29621.png)

```python
headers = {
        'Referer': "https://passport.weibo.cn/signin/login?entry=mweibo&res=wel&wm=3349&r=https://m.weibo.cn/compose/",
        'User-Agent': "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Mobile Safari/537.36"
        }
```

### **获取登入参数**

![](http://cdn.zhaojingyi0126.com/IMG/17569167-e23fb69490ae5284.png)

```python
params = {
        'username': '******',
        'password': '*******',
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
```

### 登入微博

```python
import requests

# 登入微博网址
Request_URL = "https://passport.weibo.cn/sso/login"

# 登入头文件
Request_Headers = {
        'Referer': "https://passport.weibo.cn/signin/login?entry=mweibo&res=wel&wm=3349&r=https://m.weibo.cn/compose/",
        'User-Agent': "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Mobile Safari/537.36"
        }

# 登入参数
Form_Data = {
        'username': '*****',
        'password': '*****',
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

res = requests.post(Request_URL, data=Form_Data, headers=Request_Headers)
print(res)
```

### 保留登入状态

```python
#  使用session保存登入状态
session = requests.Session()
session.headers.update(headers)
res = session.post(URL_login, data=params)
```

## 发微博

先手动发一条微博，然后看看是哪个网址在响应

![](http://cdn.zhaojingyi0126.com/image-20200430121510442.png)

可以在`Form Data` 中看到发送的详情

![](http://cdn.zhaojingyi0126.com/image-20200430121550050.png)

我们可以构造一个评论参数，`content`是微博的内容，然后我们去找找 `st` 在哪

```python
Content_Data = {
  'content': '本条微博由 Python 发送',
  'st': st
}
```

### st

鼠标右键点击 **显示网页源代码**，然后 **ctrl + f** 搜索请求里的 `st` 值，我们可以用各种之前学过的方法，把这个数据匹配出来

![image-20200430122125212](http://cdn.zhaojingyi0126.com/image-20200430122125212.png)

或者我们再找找网页，看看有没有这个参数。我们发现，`config` 里面有这个参数呢~

![image-20200430122408560](http://cdn.zhaojingyi0126.com/image-20200430122408560.png)

```python
Request_Config = session.get('https://m.weibo.cn/api/config')
Config = Request_Config.json()
st = Config['data']['st']
```

### 完整代码

```python
import requests

# 登入微博网址
RequestURL = "https://passport.weibo.cn/sso/login"

# 登入头文件
RequestHeaders = {
        'Referer': "https://passport.weibo.cn/signin/login?entry=mweibo&res=wel&wm=3349&r=https://m.weibo.cn/compose/",
        'User-Agent': "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Mobile Safari/537.36"
        }

# 登入参数
FormData = {
        'username': '********',
        'password': '*****',
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

# 评论网址
RequestComment = "https://m.weibo.cn/api/statuses/update"

# 获取st值
RequestConfig = LoginSession.get('https://m.weibo.cn/api/config')
Config = RequestConfig.json()
st = Config['data']['st']

# 构造微博参数
DataCompose = {
  'content': '本条微博由 Python 发送',
  'st': st
}

# 发表微博
ResCompose = LoginSession.post('https://m.weibo.cn/api/statuses/update', data=DataCompose)
print(ResCompose.status_code)
```

可以加上函数，重写一下这个代码

```python
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

LoginSession = Login("******","********")
SendContent(LoginSession,"本条微博由Python发送")
```

## 微博点赞

### 获取微博列表

以扇贝网微博为例（https://m.weibo.cn/u/2139359753）

```python
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
```

### 点赞

```python
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
```

### 批量点赞

```python
for i in WeiBoList:
    # card_type=9的时候，是一个正常的微博
    if i['card_type'] == 9:
        SendHeart(LoginSession,i['mblog']['id'])
```

也可以写成一个函数

```python
def SendHeartAll(LoginSession):
    WeiBoList = GetList(LoginSession)
    for i in WeiBoList:
        # card_type=9的时候，是一个正常的微博
        if i['card_type'] == 9:
            SendHeart(LoginSession,i['mblog']['id'])
```

### 完整代码

```python
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

LoginSession = Login("**********","**********")
SendContent(LoginSession,"本条微博由Python发送")
SendHeartAll(LoginSession)
```

## 发表评论

```python
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
```

### 批量评论

```python
def SendCommentAll(LoginSession,Comment): 
    WeiBoList = GetList(LoginSession)
    for i in WeiBoList:
        # card_type=9的时候，是一个正常的微博
        if i['card_type'] == 9:
            SendComment(LoginSession,Comment,i['mblog']['id'])
```

## 完整代码

```python
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
           
LoginSession = Login("***********","**********")
SendContent(LoginSession,"本条微博由Python发送")
SendHeartAll(LoginSession)
Comment = "给扇贝Python课程点赞，此留言由Python自动发送"
SendCommentAll(LoginSession,Comment)
```



