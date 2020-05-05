> 本单元视频链接（上）：https://v.youku.com/v_show/id_XNDY1MjcxNjA5Ng==.html
>
> 上面的视频包含豆瓣保存数据+QQ音乐的内容
>
> 本单元视频链接（下）：https://v.youku.com/v_show/id_XNDY1NDMwNjk0OA==.html

# QQ音乐评论

> 有些小伙伴反馈，对于爬虫的完整流程，还是不清楚，这边就按顺序，给大家梳理一下

## 反爬

首先查看一下，我们要爬取的网页，是否反爬（各种侵害人家服务器的事情，我们不能干）

QQ音乐网址：https://y.qq.com

要查看该网页的反爬要求，可以直接在网页后加`/robots.txt`

QQ音乐反爬要求就是：https://y.qq.com/robots.txt

看了一下官网不给爬的内容，没有说不可以爬评论，那我们就爬了~

![image-20200421092635250](http://cdn.zhaojingyi0126.com/image-20200421092635250.png)

今天我们爬虫，以QQ音乐，[杨千嬅的《野孩子》](https://y.qq.com/n/yqq/song/004FEV6D1yMdSj.html)为例，爬取评论

## 查看网页源代码

给大家回顾以下，静态网页是怎么爬取的？

1、用`requests.get`获取数据

2、确定网页返回码是`200`

3、查看一下数据，你要的数据，是不是都出来了

4、解析一下数据，用`beautifulsoup`库、正则化表达、字符串切割等方法处理数据

5、把数据保存下来

根据我们之前的操作，我们会先**右击**看一下网页源代码。

如果我们要的内容，就在源代码里面，那万事大吉，直接按照我们之前爬豆瓣的那一套来

但是我们爬QQ音乐的时候，很悲伤的发现，网页源代码里面，没有数据了！！！

（只有一大堆看不懂的英文，连个中文字都没了！）

怎么办呢？我们去找，这个评论数据在哪里

## 获取网址

现在我们去找数据，和数据对应的网址

### XHR

**XHR** 全称 **XMLHttpRequest**，它是浏览器内置的对象，使得 JavaScript 可以发送 HTTP 请求。

我们先右击打开“审查元素”，勾选Network—>勾选XHR—>查找我们要的内容

理论上，我们可以双击Name列表中的链接，一个一个找

有个小技巧，包含评论数据的东西，应该是比较大的，不至于只有几个B

![image-20200421095231875](http://cdn.zhaojingyi0126.com/image-20200421095231875.png)

所以我们翻了一下，发现有个链接有8.8KB，感觉相对大一点，我们打开链接看一下

![image-20200421095918073](http://cdn.zhaojingyi0126.com/image-20200421095918073.png)

看到了`comment`。没错，是了，数据就在里面

![image-20200421100043089](http://cdn.zhaojingyi0126.com/image-20200421100043089.png)

可以看到，这里面就包含了昵称、评论等内容

敏感一点的同学可以意识到，这其实就是一个**字典**啊！

我们点会到`Headers`，看一下这个网址，网址的获取方式是`GET`

![](http://cdn.zhaojingyi0126.com/image-20200421100305227.png)

我们先用这个网址，发现这时候，就已经包含评论数据了

```python
import requests

headers = {
  'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
}
res = requests.get('https://c.y.qq.com/base/fcgi-bin/fcg_global_comment_h5.fcg?g_tk_new_20200303=5381&g_tk=5381&loginUin=0&hostUin=0&format=json&inCharset=utf8&outCharset=GB2312&notice=0&platform=yqq.json&needNewCode=0&cid=205360772&reqtype=2&biztype=1&topid=1406731&cmd=8&needmusiccrit=0&pagenum=0&pagesize=25&lasthotcommentid=&domain=qq.com&ct=24&cv=10101010', headers=headers)

print(res.text)
```

### 参数

然后我们来重写这个网址，其实网址后面那一串参数，在`Query String Parameters`

![](http://cdn.zhaojingyi0126.com/image-20200421102029975.png)

把网址写法改一下，参数加上去

```python
import requests

headers = {
  'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
}
params = {
        'g_tk_new_20200303': '5381',
        'g_tk': '5381',
        'loginUin': '0',
        'hostUin': '0',
        'format': 'json',
        'inCharset': 'utf8',
        'outCharset': 'GB2312',
        'notice': '0',
        'platform': 'yqq.json',
        'needNewCode': '0',
        'cid': '205360772',
        'reqtype': '2',
        'biztype': '1',
        'topid': '1406731',
        'cmd': '8',
        'needmusiccrit': '0',
        'pagenum':'0',
        'pagesize': '25',
        'lasthotcommentid': '',
        'domain': 'qq.com',
        'ct': '24',
        'cv': '10101010'
        }
res = requests.get('https://c.y.qq.com/base/fcgi-bin/fcg_global_comment_h5.fcg', headers=headers, params=params)
print(res.text)
```

## 处理数据

### JSON

**JSON**（JavaScript Object Notation）是一种轻量级的数据交换格式。 它的本质，是一个字符串，然后里面可能是字典，也可能是列表。

```python
# 字典
dict = {'pagesize': 25}

# JSON
json = '{"pagesize": 25}'

# 列表
list = ['x', 'y', 'z']

# JSON
json = '["x", "y", "z"]'
```

我们需要用`.json()`来转换

为什么需要转换，而不是直接就是个字典？

因为 **JSON**是一种通用格式，不仅适用于Python，其他语言可以用。只是在Python里，它对应的是字典和列表

```python
data = res.json()  # data是字典格式
```

处理字典数据，是我们熟悉的部分

![](http://cdn.zhaojingyi0126.com/image-20200421103719668.png)

```python
for item in data['comment']['commentlist']:
  print('{}：{}'.format(item['nick'], item['rootcommentcontent']))
```

至此，我们就把第一页的数据读出来了，完整代码如下

```python
import requests

headers = {
  'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
}
params = {
        'g_tk_new_20200303': '5381',
        'g_tk': '5381',
        'loginUin': '0',
        'hostUin': '0',
        'format': 'json',
        'inCharset': 'utf8',
        'outCharset': 'GB2312',
        'notice': '0',
        'platform': 'yqq.json',
        'needNewCode': '0',
        'cid': '205360772',
        'reqtype': '2',
        'biztype': '1',
        'topid': '1406731',
        'cmd': '8',
        'needmusiccrit': '0',
        'pagenum':'0',
        'pagesize': '25',
        'lasthotcommentid': '',
        'domain': 'qq.com',
        'ct': '24',
        'cv': '10101010'
        }
res = requests.get('https://c.y.qq.com/base/fcgi-bin/fcg_global_comment_h5.fcg', headers=headers, params=params)

data = res.json()

# 这是[最新评论]列表
for item in data['comment']['commentlist']:
  print('{}：{}'.format(item['nick'], item['rootcommentcontent']))

# 这是[精彩评论]列表
for item in data['hot_comment']['commentlist']:
  print('{}：{}'.format(item['nick'], item['rootcommentcontent']))
```

### 翻页

经过观察，我们发现，每次翻页，`Query String Parameters` 里面，只有两个参数变了。

其中`pagenum`比较好理解，就是每一次翻页，数字加一

![](http://cdn.zhaojingyi0126.com/image-20200428211433246.png)

我们重点来找一下，`lasthotcommentid` 这个参数在哪里

发现这个单词，就是`last hot comment id`，最后一个评论的ID

因为QQ音乐有两种评论，**最新评论**和**精彩评论**，我们不确定到底是哪个ID，所以我们需要翻页确认一下

我们观察一下`data['comment']`和`data['hot_comment']`，最后发现，数据在`data['comment']`中

```python
import requests
import time

headers = {
  'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
}
# 第一次 lasthotcommentid 为空
lasthotcommentid = ''
# 前五页
for pagenum in range(5):
    params = {
            'g_tk_new_20200303': '5381',
            'g_tk': '5381',
            'loginUin': '0',
            'hostUin': '0',
            'format': 'json',
            'inCharset': 'utf8',
            'outCharset': 'GB2312',
            'notice': '0',
            'platform': 'yqq.json',
            'needNewCode': '0',
            'cid': '205360772',
            'reqtype': '2',
            'biztype': '1',
            'topid': '1406731',
            'cmd': '8',
            'needmusiccrit': '0',
            'pagenum': pagenum,
            'pagesize': '25',
            'lasthotcommentid': lasthotcommentid,
            'domain': 'qq.com',
            'ct': '24',
            'cv': '10101010'
            }
    res = requests.get('https://c.y.qq.com/base/fcgi-bin/fcg_global_comment_h5.fcg', headers=headers, params=params)
    data = res.json()
    print('==================================\n爬虫QQ音乐：{}第{}页\n=================================='.format(data['topic_name'],pagenum+1))
    for item in data['comment']['commentlist']:
        print('{}：{}'.format(item['nick'], item['rootcommentcontent']))
    
    # 当前页最后一个评论的 commentid 作为下一页的 lasthotcommentid
    lasthotcommentid = data['comment']['commentlist'][-1]['commentid']
    
    # 防止爬取太快被封
    time.sleep(1)
```

## 保存数据

```python
import requests
import time
import xlwt  

headers = {
  'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
}
lasthotcommentid = ''
params = {
        'g_tk_new_20200303': '5381',
        'g_tk': '5381',
        'loginUin': '0',
        'hostUin': '0',
        'format': 'json',
        'inCharset': 'utf8',
        'outCharset': 'GB2312',
        'notice': '0',
        'platform': 'yqq.json',
        'needNewCode': '0',
        'cid': '205360772',
        'reqtype': '2',
        'biztype': '1',
        'topid': '1406731',
        'cmd': '8',
        'needmusiccrit': '0',
        'pagenum': 0,
        'pagesize': '25',
        'lasthotcommentid': lasthotcommentid,
        'domain': 'qq.com',
        'ct': '24',
        'cv': '10101010'
        }

def GetComment(headers, params):
    res = requests.get('https://c.y.qq.com/base/fcgi-bin/fcg_global_comment_h5.fcg', headers=headers, params=params)
    data = res.json()
    return data

workbook = xlwt.Workbook()     
row = 1
for pagenum in range(5):    
    params['pagenum'] = pagenum
    params['lasthotcommentid'] = lasthotcommentid
    data = GetComment(headers, params)
    print('爬虫QQ音乐：{}第{}页'.format(data['topic_name'],pagenum+1))    
    if pagenum == 0:        
        sheet = workbook.add_sheet(data['topic_name'])  
        head = ['昵称', '评价'] 
        for h in range(len(head)):
            sheet.write(0, h, head[h])            
    for item in data['comment']['commentlist']:
        sheet.write(row, 0, item['nick'])
        sheet.write(row, 1, item['rootcommentcontent'])    
        row += 1
    lasthotcommentid = data['comment']['commentlist'][-1]['commentid']
    time.sleep(1)
    
workbook.save('QQ音乐评论.xls')  
print('写入excel成功')
```

# 网易云音乐

## 获取单页数据

以[《我和我的祖国》](https://music.163.com/#/song?id=1392990601)为例，流程就是：

- 找到你要获取的网页
- 右击“检查”，获取`headers `，记得把`refere`r和`user-agent`都贴下来

- `params `和`encSecKey`也都复制下来
  ![`params `和`encSecKey`](http://cdn.zhaojingyi0126.com/IMG/17569167-21514629da6f02d1.png)

你可以看到所有的评论信息都在`content`里面

![](http://cdn.zhaojingyi0126.com/IMG/17569167-dfbd1c8f6a3576c1.png)

代码里面，只输出了一条信息，你想输出全部，加个`for`循环就好

```python
import requests

headers = {
        'referer': 'https://music.163.com/song?id=1392990601',
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'
}

params = {
        "params": "uDLzYGLcTNCjLjdCW+9IichJlH11qTKrVpnGQoJy6sFBtlEovOycsJ8CZZ+BKvM31A9o60Ur69YS1sCQiiI8ySaGicLsHF2L69/Fb/7msPFRCeXt2L//zPjdd4JbHqThXk/yD5UUmb4nF2jfXO8pkWyNJUSgKrCM4/1hPCbOd3oIX+F0ThM4D9J9yg8DVSVD",
        "encSecKey": "4ad59dea31c7272fa1cfb8ba95bb55ca77947327398f46b1cb30ca0dfdb55a6241d3ec670965b203ab48c3cc453f98c2542399a5d9112920e03d0e291ef26f9c24327c5dedca61d5776065862cfa1cf99c0a692db4c83e33f9052ab1cec047a1f992bfc8a91bd2d8f30dd01bd1ab884c5d3622d4b034e5c4c9d10eba91a11784"
        }

url = "https://music.163.com/weapi/v1/resource/comments/R_SO_4_1392990601?csrf_token="
res = requests.post(url, headers=headers, params=params)
data = res.json()

print(data['hotComments'][0]['content'])
```

## 翻页

由于数据加密，太过复杂，不属于基础课程的内容。感兴趣的同学可以移步：

[知乎：如何爬网易云音乐的评论数？](https://www.zhihu.com/question/36081767/answer/140287795)

[Python爬虫爬取网易云音乐全部评论](https://www.jianshu.com/p/98e33aae1d6b)

