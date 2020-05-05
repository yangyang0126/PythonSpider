# Python Spider

爬虫基本流程是：获取网页数据，处理网页数据，保存处理后的数据

## 获取网页数据

获取网页最难的地方，是获取到真正的网页地址。

我们可以右击“查看源代码”，如果网页内容里，包含你想要的部分，那超开心，直接复制网址就好了。但是一般情况下，我们会发现，原代码里面，很多信息是没有的。

举个例子，如果你打开[豆瓣排行榜](https://book.douban.com/top250?start=0)，你会发现，网页源代码里面，就有每一本书籍的信息。那就好了，你不需要搞什么复杂的操作，直接`get`网址就好了.

但是如果我们打开QQ音乐[等你下课](https://y.qq.com/n/yqq/song/001J5QJL1pRQYB.html)详情页，我们会看到，网页源代码里面，并没有评论信息。那这就需要我们想办法去获取了。

还有一种情况，类似淘宝、微博等网站，有些信息，需要你账号密码登入后才能看，那就会麻烦一点。如果涉及到图像验证什么，那就会更更麻烦。

不过，兵来将挡，水来土掩，我们总会搞定哒~



## 处理网页数据

BeautifulSoup库：包括解析数据和提取数据

re库：用正则化表达提取信息





## 保存网页数据

openpyxl库

xlwt库





## 举个例子



**静态网站**

获取本地文件ISMRM目录：urllib.request+re+os+xlwt

获取豆瓣读书排行榜：requests+BeautifulSoup+xlwt

获取扇贝打卡记录：urllib.request+re+xlwt

获取扇贝单词书：urllib.request+re+xlwt

统计扇贝半年打卡记录：urllib.request+re+xlwt+datetime

单词群打卡：urllib.request+re+xlwt+datetime

制作单词量测试软件：requests+easygui+xlwt



**动态网页**

获取扇贝炼句数据（包含账号密码登入）：requests+json+re+xlwt