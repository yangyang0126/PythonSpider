# 写在前面的话

之前给大家写过一个非常基础的Python教程

[Python爬虫详细教程：统计扇贝网站打卡数据](https://www.jianshu.com/p/16bcce239ee6)

这个爬虫教程稍微升级了一点点：

- `re.findall`精确匹配和跨行匹配
- 实现最傻瓜的翻页方式（高级的我还不会）
- 构建了简单的函数



# 代码运行图

先上代码运行图

![](C:\Users\Administrator\AppData\Roaming\Typora\typora-user-images\1558691252165.png)

这是运行结果，Excel的格式没改（我技术还不行）

![](C:\Users\Administrator\AppData\Roaming\Typora\typora-user-images\1558691588244.png)

# 整体思路

1、爬虫网址：扇贝网单词书https://www.shanbay.com/wordbook/202/

注意看，`https://www.shanbay.com/wordbook/`这部分都是一样的，关键就是`202`这个数字不一样，每一个单词书，有自己的数字

![](C:\Users\Administrator\AppData\Roaming\Typora\typora-user-images\1558676692964.png)

一本单词书，有很多个Unit

![](C:\Users\Administrator\AppData\Roaming\Typora\typora-user-images\1558677426247.png)

2、通过该网址，爬虫得到每一个Unit的网址：https://www.shanbay.com/wordlist/202/16306/

注意看，`https://www.shanbay.com/wordlist/`这部分都是一样的，`202`代表单词书，`16306`代表Unit

![](C:\Users\Administrator\AppData\Roaming\Typora\typora-user-images\1558676748647.png)

所以首先，爬虫，把我们要找的单词书的所有Unit的网址读出来

![](C:\Users\Administrator\AppData\Roaming\Typora\typora-user-images\1558677278260.png)

3、翻页

每一个Unit，有好几页的单词，所以我们需要翻页

![](C:\Users\Administrator\AppData\Roaming\Typora\typora-user-images\1558677549010.png)

我们在网页源代码看到，它首先计算，一页20个单词，158个单词要放几页

然后就在网址后面加`?page=`，如果是第一页，就是`?page=1`，第二页就是`?page=2`，以此类推

https://www.shanbay.com/wordlist/202/16306/?page=1

所以，这个由单词书`202`，Unit`16306`，页数`Page=1`组成的网址，才是我们最后要爬取的网页

![](C:\Users\Administrator\AppData\Roaming\Typora\typora-user-images\1558677847281.png)

4、爬虫部分不再赘述，可参考上一篇，依旧是读取数据，存到Excel

5、唯一需要注意的是，我们用到了Excel功能，需要我们需要安装Excel的相关库

打开命令提示符：`附件`—`命令提示符`

![](https://upload-images.jianshu.io/upload_images/17569167-b2fab6cda27ccbb9.png?imageMogr2/auto-orient/)

输入

```python
pip install xlwt
```

装好之后，你再次输入这行代码，应该显示如下

![](C:\Users\Administrator\AppData\Roaming\Typora\typora-user-images\1558690508827.png)



# 稍微进阶一下

正则化`re.findall`

上一次已经讲到用`re.findall`可以找到我们想要的关键词，今天补充2个知识点

1、`（）`的神奇用法

不加`（）`的时候，字符串就是从`<strong>`匹配到`<strong>`

```Python
find_word = re.findall("<strong>[a-z,A-Z]*?</strong>",web_word) 
```

![](C:\Users\Administrator\AppData\Roaming\Typora\typora-user-images\1558675954670.png)

加上`（）`，字符串只匹配`<strong>`和`<strong>`中间的内容

````python
find_word = re.findall("<strong>[a-z,A-Z]*?</strong>",web_word) 
````

![](C:\Users\Administrator\AppData\Roaming\Typora\typora-user-images\1558676081080.png)

2、多行匹配

![](C:\Users\Administrator\AppData\Roaming\Typora\typora-user-images\1558676231165.png)

我们在网站中发现，我们要匹配的内容，从`<td class="span10"`到`</td>`不在同一行。用默认的方式匹配，会匹配失败

这时候，我们在`re.findall`最后加上`re.S`

```python
find_meaning = re.findall("<td class=\"span10\"> (.*?)</td>",web_word,re.S) 
```

这样得到的信息，就是完整的

![](C:\Users\Administrator\AppData\Roaming\Typora\typora-user-images\1558676353955.png)



# 完整代码

```python
# -*- coding: utf-8 -*-
"""
Created on Fri May 24 2019

@author: YangYang
"""

'''
web_shanbay：扇贝网址
web_number：单词书编号
web_wordbook：单词书网址
web_wordlist：单词书——Unit网址
web_wordpage：单词书——Unit——分页网址

web_wordbook_data：单词书网页数据
web_wordlist_data：Unit网页数据
web_wordpage_data：Unit分页网页数据

wordlist_name：Unit名称
wordlist_id：Unit编号

'''

from urllib.request import urlopen
import re
import xlwt
import math


# 获取单词书网页数据
def FindWordbookData(web_number):    
    web_shanbay = "https://www.shanbay.com/wordbook/"
    web_wordbook = web_shanbay + str(web_number) + "/"
    web_wordbook = urlopen(web_wordbook)
    web_wordbook_data = web_wordbook.read().decode()
    return web_wordbook_data

# 定位该单词书所有的Unit和对应网址
def FindWebWordlist(web_number,web_wordbook_data): 
    find_address = "<a href=\"/wordlist/" + str(web_number) + ".*?</a>"
    find_wordlist = re.findall(find_address,web_wordbook_data) 
    # 获取Unit和网址
    wordlist_id = []
    wordlist_name = []
    web_wordlist = []
    for wordlist in find_wordlist:
        ID = wordlist.split('/')[3]
        name = wordlist.split('>')[1]
        name = name[:-3]
        wordlist_name.append(name)
        wordlist_id.append(ID)
        web_wordlist.append("https://www.shanbay.com/wordlist/" + str(ID) + "/")
    return web_wordlist

# 获取网页取读数据
def ReadWebData(web):    
    web_read = urlopen(web)
    web_read = web_read.read().decode()
    return web_read

# 获取页数
def CalPage(web_data):
    wordlist_num_vocab = re.findall("wordlist-num-vocab\">([0-9]*?)<",web_data)
    var_pages = math.ceil(float(wordlist_num_vocab[0])/20)
    return var_pages

# 获取标题
def FindTitle(web_data):
    web_title = re.findall("<title>单词书： (.*?) </title>",web_data)
    return web_title


a = '''
部分单词书编号：
TOEFL核心词汇21天突破:202
扇贝托业词汇精选:91918
扇贝循环单词书·六级（乱序）:197656
'''
print(a)
web_number = input("请输入单词书编号:")
#web_number = 202 #这里需要根据你想爬取的单词书，需要改
web_wordbook_data = FindWordbookData(web_number)    
web_wordlist = FindWebWordlist(web_number,web_wordbook_data)
print('\n')
print("正在取读数据")

# 定义保存Excel的位置
workbook = xlwt.Workbook()  #定义workbook    


for wordlist in web_wordlist:    
    web_wordlist_data = ReadWebData(wordlist)
    
    # 打开Excel，保存Sheet和表头
    title = re.findall("<title>词串：  (.*?) </title>",web_wordlist_data)
    sheet = workbook.add_sheet(str(title[0]))  #添加sheet  
    head = ['单词', '解释']    #表头
    for h in range(len(head)):
       sheet.write(0, h, head[h])    #把表头写到Excel里面去
    m = 1 #定义Excel的行数    
    
    # 获取Unit的页码和相应内容
    var_pages = CalPage(web_wordlist_data)
    for i in range(1,var_pages+1):
        web_wordpage = str(wordlist) + "?page=" + str(i)    
        web_wordpage_data = ReadWebData(web_wordpage)
    
        # 开始获取单词和解释
        find_word = re.findall("<strong>([a-z,A-Z]*?)</strong>",web_wordpage_data) 
        find_meaning = re.findall("<td class=\"span10\">(.*?)</td>",web_wordpage_data,re.S) 
        find_result = zip(find_word,find_meaning) 
        for word,meaning in find_result:            
            sheet.write(m, 0, word)
            sheet.write(m, 1, meaning)
            m += 1            

SaveAddress = FindTitle(web_wordbook_data)
SaveAddress = str(SaveAddress[0]) + ".xls"
workbook.save(SaveAddress)
print('\n') 
print('写入excel成功')
print("文件位置：和你的代码在一个文件夹下面")
print('\n') 
input("取读完毕，点击回车退出") 
```

# 最后

1、不保证每一个单词书都能取读，各别好像不行（还在思考为什么）

2、Excel文档和你的代码会在一个目录下面，你也可以自己改路径

![](C:\Users\Administrator\AppData\Roaming\Typora\typora-user-images\1558691431753.png)

3、Excel比较丑，麻烦大家自己手动调一调（因为我还不会写代码改格式）

有任何问题，欢迎大家给我留言。这是小白给小白的教程~