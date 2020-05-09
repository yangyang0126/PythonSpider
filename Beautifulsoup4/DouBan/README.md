# 爬取豆瓣电影排行榜

回顾一下爬虫的步骤

- 明确目标：首先确定，我们要爬虫什么内容
- 打开网页：确定网页网址，得到网页响应
- 定位数据：找到我们需要的数据
- 清洗数据：把我们要的那部分数据截出来
- 保存数据：把数据保存到EXCEL或者txt

## 明确目标

[豆瓣电影 Top 250](https://movie.douban.com/top250)，它的网址是：https://movie.douban.com/top250

## 打开网页

根据之前所学的，我们知道，获取数据，需要用到`requests`这个库。豆瓣是一个静态网页，用get获取响应

```python
import requests  # 获取网页数据

url = "https://movie.douban.com/top250"
res = requests.get(url)  # requests发起请求，静态网页用get 
print(res)

# 输出：
# <Response [418]>
```

悲伤的是，我们的响应不是200，是418，百度一下418，就是被网站的反爬程序返回了~这时候，我们需要构造一个头文件，就是让计算机觉得，是人在操作，而不是机器在操作

![](http://cdn.zhaojingyi0126.com/image-20200417205750006.png)

在`Requests Headers`里面，把`User-Agent` 的内容贴上去

```python
import requests  # 获取网页数据

url = "https://movie.douban.com/top250"

headers = {
  'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
}

res = requests.get(url, headers=headers)  # requests发起请求，静态网页用get 
print(res)

# 输出：
# <Response [200]>
```

这时候就成功获得了200的返回码

## 解析数据

解析和提取数据，我们需要用到`beautifulsoup`这个库

安装`beautifulsoup`，详情可戳：https://pypi.org/project/beautifulsoup4/

```
pip install beautifulsoup4
```

解析数据

```python
import requests  
from bs4 import BeautifulSoup  # 导入BeautifulSoup类

url = "https://movie.douban.com/top250"
headers = {
  'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
}
res = requests.get(url, headers=headers)  
soup = BeautifulSoup(res.text, 'html.parser')  # 解析数据
# 第一个参数为网页源代码，第二个参数为解析器
```

## 提取数据

`.find(html标签, html属性)`：返回符合条件的**第一个**数据（列表格式）

`.find_all(html标签, html属性)`：返回符合条件的**所有**数据（列表格式）

先放标签，再放属性，具体放多少属性，看自己的需求

可以不停的find，一层一层往下找

```python
print(soup.find('span', class_="title"))
# 输出
# <span class="title">肖申克的救赎</span>

print(soup.find_all('span', class_="title"))
# 输出
# [<span class="title">肖申克的救赎</span>, <span class="title"> / The Shawshank Redemption</span>, <span class="title">霸王别姬</span>, <span class="title">阿甘正传</span>, <span class="title"> / Forrest Gump</span>, <span class="title">这个杀手不太冷</span>, <span class="title"> / Léon</span>, <span class="title">美丽人生</span>, <span class="title"> / La vita è bella</span>, <span class="title">泰坦尼克号</span>, <span class="title"> / Titanic</span>, <span class="title">千与千寻</span>, <span class="title"> / 千と千尋の神隠し</span>, <span class="title">辛德勒的名单</span>, <span class="title"> / Schindler's List</span>, <span class="title">盗梦空间</span>, <span class="title"> / Inception</span>, <span class="title">忠犬八公的故事</span>, <span class="title"> / Hachi: A Dog's Tale</span>, <span class="title">海上钢琴师</span>, <span class="title"> / La leggenda del pianista sull'oceano</span>, <span class="title">楚门的世界</span>, <span class="title"> / The Truman Show</span>, <span class="title">三傻大闹宝莱坞</span>, <span class="title"> / 3 Idiots</span>, <span class="title">机器人总动员</span>, <span class="title"> / WALL·E</span>, <span class="title">放牛班的春天</span>, <span class="title"> / Les choristes</span>, <span class="title">星际穿越</span>, <span class="title"> / Interstellar</span>, <span class="title">大话西游之大圣娶亲</span>, <span class="title"> / 西遊記大結局之仙履奇緣</span>, <span class="title">熔炉</span>, <span class="title"> / 도가니</span>, <span class="title">疯狂动物城</span>, <span class="title"> / Zootopia</span>, <span class="title">无间道</span>, <span class="title"> / 無間道</span>, <span class="title">龙猫</span>, <span class="title"> / となりのトトロ</span>, <span class="title">教父</span>, <span class="title"> / The Godfather</span>, <span class="title">当幸福来敲门</span>, <span class="title"> / The Pursuit of Happyness</span>, <span class="title">怦然心动</span>, <span class="title"> / Flipped</span>, <span class="title">触不可及</span>, <span class="title"> / Intouchables</span>]
```

Spyder会提示用法

![](http://cdn.zhaojingyi0126.com/image-20200417212150052.png)

**注：以下定位方法都不是唯一的，只要能出结果就可以的。要怎么定位，可以根据自己的习惯来**

获取标题，这时候有些电影有英文名，也同时输出了

```python
items = soup.find_all('span', class_="title")
for i in items:
    print(i.text)
```

获取每一部电影的推荐语

```python
items = soup.find_all('span', class_="inq")
for i in items:
    print(i.text)
```

获取评分

```python
items = soup.find_all('span', class_="rating_num")
for i in items:
    print(i.text)
```

获取电影导演等详情（先缩小范围，再查找）

```python
content = soup.find_all('ol', class_="grid_view")
items = content[0].find_all('div', class_="bd")
for i in items:
    print(i.find('p', class_="").text)
```

获取标题和电影链接

```python
items = soup.find_all('div', class_="hd")
for i in items:
    link = i.find('a')['href']
    title = i.find('span', class_='title').text
    print(title, link)
```

进阶一点，我们可以用CSS选择器，**#** 代表 id，**.** 代表 class

比如获取电影导演详情，刚刚我们是这么写的

```python
content = soup.find_all('ol', class_="grid_view")
items = content[0].find_all('div', class_="bd")
for i in items:
    print(i.find('p', class_="").text)
```

我们现在可以这么写

```python
items = soup.select('ol.grid_view div.bd')
for i in items:
    print(i.find('p', class_="").text)
```

其中，用空格代表层级

## 实践

我们在基础课**【3.11节，字符串】**的实践，输出[豆瓣电影 Top 250](https://movie.douban.com/top250)，前25部电影详情

当时是这么写的

```python
text = open('D:/Python/html_text.txt', 'rb')
text = text.read().decode('utf-8')
movies = text.split('class="grid_view\">')[1].split('<li>')  #movies此时是一个列表

for i in range(1,len(movies)):
    movie = movies[i]    # 把movies这个列表的值，依次取出
    title = movie.split('</span>')[0].split('>')[-1]
    rate = movie.split('v:average\">')[1].split('</span>')[0]
    number = movie.split('star')[1].split('<span>')[1].split('</span>')[0]
    quote = movie.split('inq')[1].split('>')[1].split('<')[0]
    year = movie.split(' <p class="">')[1].split('<br>')[1].split('&nbsp')[0].strip()
    print("{},《{}》，豆瓣评分{}，{}。推荐理由：{}".format(year,title, rate, number, quote))
```

![](http://cdn.zhaojingyi0126.com/IMG/image-20200409104516529.png)

我们来重写一次，顺带把电影链接加上(写法不唯一，只要能获取到数据就行)

```python
import requests  
from bs4 import BeautifulSoup  

url = "https://movie.douban.com/top250"
headers = {
  'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
}
res = requests.get(url, headers=headers)  
soup = BeautifulSoup(res.text, 'html.parser') 

items = soup.select('ol.grid_view div.item')
for i in items:
    title = i.select('span.title')[0].text
    link = i.find('a')['href']
    rate = i.find('div',class_='star').text.split('\n')[2]
    number = i.find('div',class_='star').text.split('\n')[-2]
    quote = i.select('p.quote')[0].text.split('\n')[1]
    year = i.find('p', class_="").text.split('\n')[2].strip()[:4]
    print("{},《{}》，豆瓣评分{}，{}。推荐理由：{}\n电影链接：{}\n".format(year,title, rate, number, quote, link))

# 输出：
1994,《肖申克的救赎》，豆瓣评分9.7，1984988人评价。推荐理由：希望让人自由。
电影链接：https://movie.douban.com/subject/1292052/

1993,《霸王别姬》，豆瓣评分9.6，1469016人评价。推荐理由：风华绝代。
电影链接：https://movie.douban.com/subject/1291546/

1994,《阿甘正传》，豆瓣评分9.5，1504554人评价。推荐理由：一部美国近现代史。
电影链接：https://movie.douban.com/subject/1292720/
...........
```

## 保存数据

这里要注意，用到Excel相关功能的时候，要导入相关库

```
pip install xlwt
```

具体使用方法

```python
import xlwt  # 把Excel输出模块加进来

# 定义保存Excel的位置
workbook = xlwt.Workbook()  #定义workbook
sheet = workbook.add_sheet('第一页数据')  #添加sheet
head = ['年份', '电影名称', '豆瓣评分', '评价人数', '推荐理由', '电影链接']    #表头
for h in range(len(head)):
    sheet.write(0, h, head[h])    #把表头写到Excel里面去
    
# 把内容保存到Excel
sheet.write(row, 0, year)  # 第row行，第1列
sheet.write(row, 1, title)  # 第row行，第2列
sheet.write(row, 2, rate)  # 第row行，第3列
sheet.write(row, 3, number)  # 第row行，第4列
sheet.write(row, 4, quote)  # 第row行，第5列
sheet.write(row, 5, link)  # 第row行，第6列

# 保存Excel表
workbook.save('豆瓣电影排行榜.xls')  # 和代码在一个路径下
print('写入excel成功')
```

完整代码

```python
import requests  
from bs4 import BeautifulSoup  # 导入BeautifulSoup函数
import xlwt  # 把Excel输出模块加进来

# 定义保存Excel的位置
workbook = xlwt.Workbook()  # 定义workbook
sheet = workbook.add_sheet('第一页数据')  # 添加sheet
head = ['年份', '电影名称', '豆瓣评分', '评价人数', '推荐理由', '电影链接'] # 表头
for h in range(len(head)):
    sheet.write(0, h, head[h])    # 把表头写到Excel里面去，从0开始
row = 1 # 第2行（第一行是0）
    
url = "https://movie.douban.com/top250"
headers = {
  'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
}
res = requests.get(url, headers=headers)  
soup = BeautifulSoup(res.text, 'html.parser') 

items = soup.select('ol.grid_view div.item')
for i in items:
    title = i.select('span.title')[0].text
    link = i.find('a')['href']
    rate = i.find('div',class_='star').text.split('\n')[2]
    number = i.find('div',class_='star').text.split('\n')[-2]
    quote = i.select('p.quote')[0].text.split('\n')[1]
    year = i.find('p', class_="").text.split('\n')[2].strip()[:4]
    print("{},《{}》，豆瓣评分{}，{}。推荐理由：{}\n电影链接：{}\n".format(year, title, rate, number, quote, link))
    # 把内容保存到Excel
    sheet.write(row, 0, year)  # 第row行，第1列
    sheet.write(row, 1, title)  # 第row行，第2列
    sheet.write(row, 2, rate)  # 第row行，第3列
    sheet.write(row, 3, number)  # 第row行，第4列
    sheet.write(row, 4, quote)  # 第row行，第5列
    sheet.write(row, 5, link)  # 第row行，第6列
    row += 1

# 保存Excel表
workbook.save('豆瓣电影排行榜.xls')  # 和代码在一个路径下
print('写入excel成功')
```

![](http://cdn.zhaojingyi0126.com/image-20200419231040858.png)

这时候，Excel表格是没有任何格式的，想要设置单元格样式的小伙伴，请戳：[利用xlwt设置Excel单元格格式](Python/2.md)

## 翻页

首先，我们在网站上翻几页看看网址有没有什么规律，我们发现它的网址，就是最后有一个0、25、50的数字在变化。每翻一页，数字增加25

https://movie.douban.com/top250?start=0&filter=

https://movie.douban.com/top250?start=25&filter=

https://movie.douban.com/top250?start=50&filter=

自然而然，我们想到可以来个for循环

```python
url = 'https://movie.douban.com/top250?start={}&filter='
urls = [url.format(num * 25) for num in range(10)]
```

另外，我们可以构建一些函数，让整个代码变得更流畅

```python
import requests  
from bs4 import BeautifulSoup  # 导入BeautifulSoup函数
import xlwt  # 把Excel输出模块加进来

# 定义保存Excel的位置
workbook = xlwt.Workbook()  # 定义workbook
sheet = workbook.add_sheet('数据')  # 添加sheet
head = ['年份', '电影名称', '豆瓣评分', '评价人数', '推荐理由', '电影链接'] # 表头
for h in range(len(head)):
    sheet.write(0, h, head[h])    # 把表头写到Excel里面去，从0开始

def GetRes(url):     
    headers = {
      'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
    }
    res = requests.get(url, headers=headers)  
    soup = BeautifulSoup(res.text, 'html.parser') 
    return soup

url = 'https://movie.douban.com/top250?start={}&filter='
urls = [url.format(num * 25) for num in range(10)]
row = 1 # excel表格的行
for page in urls:
    soup = GetRes(page)
    items = soup.select('ol.grid_view div.item')
    for i in items:
        title = i.select('span.title')[0].text
        link = i.find('a')['href']
        rate = i.find('div',class_='star').text.split('\n')[2]
        number = i.find('div',class_='star').text.split('\n')[-2]
        try:
            quote = i.select('p.quote')[0].text.split('\n')[1]
        except:
            quote = ""    # 有些电影没有推荐语     
        year = i.find('p', class_="").text.split('\n')[2].strip()[:4]
        print(row,title)
        # 把内容保存到Excel
        sheet.write(row, 0, year)  
        sheet.write(row, 1, title)  
        sheet.write(row, 2, rate) 
        sheet.write(row, 3, number)  
        sheet.write(row, 4, quote)  
        sheet.write(row, 5, link)  
        row += 1

# 保存Excel表
workbook.save('豆瓣电影排行榜.xls')  
print('写入excel成功')
```

# 爬取豆瓣读书排行榜

## 写在前面的话

单说爬虫豆瓣排行榜，好像有点无聊~
如果说，利用我们爬取的信息，可以做一个自己的年度读书展示，会不会感觉有趣一点呢，嘻嘻~
爬取豆瓣书籍的封面图，很快就可以做一个属于自己的读书小结啦~（参照下图）

![读书展示](http://cdn.zhaojingyi0126.com/IMG/17569167-d4f8ae14b4fbbefa.png)

之前网友提示我，触发了豆瓣反爬机制， <Response [418]>。
感谢网友提醒。现已更改。——2020.01.06

## 完整代码

```python
import requests  # 获取网页数据
from bs4 import BeautifulSoup  # 解析网页数据
import time  # 设置爬虫等待时间
import xlwt


# 获取豆瓣网址并解析数据
def get_douban_books(url,num):
    headers = {
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
                } 
    res = requests.get(url,headers=headers)  # requests发起请求，静态网页用get    
    soup = BeautifulSoup(res.text, 'html.parser')
    
    m = n = j = num
    
    items_title = soup.find_all("div", class_="pl2")    
    for i in items_title:        
        tag = i.find("a")        
        # 去掉空格和换行符
        name = ''.join(tag.text.split())
        link = tag["href"]
        title_markdown = "[{}]({})".format(name,link)
        sheet.write(m, 0, title_markdown)
        m += 1
        
    items_author = soup.find_all("p", class_="pl") 
    for i in items_author:              
        author_markdown = i.text
        sheet.write(n, 1, author_markdown)
        n += 1
        
    items_image = soup.find_all("a", class_="nbg")   
    for i in items_image:        
        tag = i.find("img")
        link = tag["src"]
        image_markdown = "![]({})".format(link)
        sheet.write(j, 2, image_markdown)
        j += 1
        
# 定义保存Excel的位置
workbook = xlwt.Workbook()  #定义workbook
sheet = workbook.add_sheet('豆瓣读书')  #添加sheet
head = ['书名', '作者', '图片']    #表头
for h in range(len(head)):
    sheet.write(0, h, head[h])    #把表头写到Excel里面去
        
# 豆瓣一共有10页数据
# 先形成网址
url = 'https://book.douban.com/top250?start={}'
urls = [url.format(num * 25) for num in range(10)] 
page_num = [num * 25+1 for num in range(10)]
for i in range(10):
    get_douban_books(urls[i],page_num[i])
    # 暂停 1 秒防止访问太快被封
    time.sleep(1)

# 保存 Excel 文件
workbook.save('豆瓣读书.xls')
```

## 代码说明

上面这个代码，可以完整的爬取豆瓣读书排行榜前250本书籍的书名、作者、图片。

如果你想做一个网页，把你的书籍信息放上去，可以去网上下载一个照片墙模板。这边给大家提供一个我自己使用的（就是文章开头那种效果）[https://github.com/yangyang0126/PythonSpider/tree/master/douban](https://github.com/yangyang0126/PythonSpider/tree/master/douban)

把你爬取到的封面图链接写进网页就可以了

```python
<article class="item thumb span-1">
	<h2>追风筝的人</h2>
	<a href="images/fulls/01.jpg" class="image"><img src="https://img3.doubanio.com/view/subject/m/public/s1727290.jpg" alt=""></a>
</article>

<article class="item thumb span-1">
	<h2>解忧杂货店</h2>
	<a href="images/fulls/02.jpg" class="image"><img src="https://img3.doubanio.com/view/subject/m/public/s27264181.jpg" alt=""></a>
</article>

<article class="item thumb span-1">
	<h2>小王子</h2>
	<a href="images/fulls/03.jpg" class="image"><img src="https://img3.doubanio.com/view/subject/m/public/s1103152.jpg" alt=""></a>
</article>
```