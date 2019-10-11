# 爬虫新浪微博

## 实现功能

1、微博登入

2、发表评论

3、自动点赞

## 微博登入

打开微博客户端：https://m.weibo.cn/，右击打开”检查“（有的浏览器叫”审查元素“）

![1570671369538](README.assets/1570671369538.png)

点上图的小图标，可以切换网页版和手机版，手机版相对好爬一点

点击`Preserve log`，保留登入信息，接着输入账号密码登入。关注左侧`login`，这里面就是我们要爬取的信息。

![1570670901788](README.assets/1570670901788.png)



**获取登入网址**

![1570670216568](README.assets/1570670216568.png)

```python
URL_login = "https://passport.weibo.cn/sso/login"
```



**获取头文件**

![1570670674122](README.assets/1570670674122.png)

```python
headers = {
        'Referer': "https://passport.weibo.cn/signin/login?entry=mweibo&res=wel&wm=3349&r=https://m.weibo.cn/compose/",
        'User-Agent': "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Mobile Safari/537.36"
        }
```



**获取登入参数**

![1570670801115](README.assets/1570670801115.png)

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



**登入微博**

```python
#  使用session保存登入状态
session = requests.Session()
session.headers.update(headers)
res = session.post(URL_login, data=params)
```



## 发表评论

完整代码

```python
import requests

# 登入微博网址
URL_login = "https://passport.weibo.cn/sso/login"

# 登入头文件
headers = {
        'Referer': "https://passport.weibo.cn/signin/login?entry=mweibo&res=wel&wm=3349&r=https://m.weibo.cn/compose/",
        'User-Agent': "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Mobile Safari/537.36"
        }

# 登入参数
data_login = {
        'username': '*******',
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

#  使用session保存登入状态
session = requests.Session()
session.headers.update(headers)
req_login = session.post(URL_login, data=data_login)

# 评论网址
URL_comment = "https://m.weibo.cn/api/statuses/update"

# 获取st值
URL_st = "https://m.weibo.cn/api/config"
req_st = session.get(URL_st)
config = req_st.json()
st = config['data']['st']

# 构造评论参数
data_compose = {
  'content': '本条微博由 Python 发送',
  'st': st
}

# 实现评论功能
req_compose = session.post('https://m.weibo.cn/api/statuses/update', data=data_compose)
print(req_compose.status_code)
```

## 微博点赞

首先，我们需要找到我们要点赞的账号页面。以扇贝网为例，通过`Preview`找到发帖的具体网址

![1570694021332](README.assets/1570694021332.png)

找到对应的网址和参数内容

![1570694101537](README.assets/1570694101537.png)

![1570694132283](README.assets/1570694132283.png)

```python
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
```







ID。以扇贝网为例，ID是`2139359753`

![1570692450590](README.assets/1570692450590.png)