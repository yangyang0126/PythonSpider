网上的教程，基本上都很简单，直接上了一大段代码，和大家说程序OK了

但我初学爬虫，还是什么都看不懂

所以，这是一个特别啰嗦的教程

------------


### 完整代码

------------


Python爬虫：[获取扇贝打卡信息](http://www.zhaojingyi0126.com/post/7/)

Python爬虫：[将爬虫结果保存到Excel](http://www.zhaojingyi0126.com/post/16/)

Python爬虫：[从TXT导入数据](http://www.zhaojingyi0126.com/post/17/)

（如果你懒得看教程，可以直接看代码）

------------

### 什么是爬虫？

------------



爬虫是自动化帮我们获取网页数据的程序

简单来说，用爬虫，去获取网页数据

那么，我们大概需要这么几个步骤

*   明确目标：首先确定，我们要爬虫什么内容

*   打开网页：确定网页网址，得到网页响应

*   定位数据：找到我们需要的数据

*   清洗数据：把我们要的那部分数据截出来

*   保存数据：把数据保存到EXCEL或者txt

------------


### 明确目标

------------



我们以扇贝网为例，讲解爬虫

简单介绍一下，扇贝网是一个学英语的网站，里面有个小组，小组里的成员一起打卡

我爬虫的目标是：得到小组成员一周的打卡时间汇总，以及对应的学习内容

![markdown17569167-84e9b840e28e1d8b.jpg](http://pxpfco2u1.bkt.clouddn.com/markdown17569167-84e9b840e28e1d8b.jpg){:width="100%" align=center}

下面开始爬虫，出发！

------------


### 打开网页

------------




首先打卡网页，各个网页的网址不一样，大家要尝试去发现规律

比如扇贝网每一位同学，会有一个```ID```，我的```ID```是16888030

那我先定义我的```ID```，用```input```把我的```ID```输进去

```Python
ID = input("请输入你的扇贝ID：")
```

`web`代表网页地址，`str`将我的`ID`从数字转换成字符串。下面两种表达方式完全等效。

```Python
web = "https://www.shanbay.com/api/v1/checkin/user/"+str(ID)+"/"
web = "https://www.shanbay.com/api/v1/checkin/user/16888030/"
```

![markdownpachong1.png](http://pxpfco2u1.bkt.clouddn.com/markdownpachong1.png){:width="100%" align=center}

存在web中的网址

然后开始获取网页

```Python
from urllib.request import urlopen  # 加入urllib模块
web = "https://www.shanbay.com/api/v1/checkin/user/"+str(ID)+"/"
shanbay = urlopen(web) # 打开网址
```

`urllib` 是Python 中用于获取网页数据的模块，通过` import `调用它。我们用`urlopen`打开网址，这时候`print(shanbay)`，输出`shanbay`的内容

![markdown17569167-f7d20c207482a6ac.webp.jpg](http://pxpfco2u1.bkt.clouddn.com/markdown17569167-f7d20c207482a6ac.webp.jpg){:width="100%" align=center}

我们可以看到“Response”，代表我们成功获得了对方网址给我们的回答

那回答的内容是什么呢？通过read打开网址

```Python
shanbay_data = shanbay.read().decode()
```

这时候输出```shanbay_data```，可以看到网页内容已经被读取

![markdown17569167-11251cff7731d443.webp.jpg](http://pxpfco2u1.bkt.clouddn.com/markdown17569167-11251cff7731d443.webp.jpg){:width="100%" align=center}

------------


### 定位数据

------------

网页已经读取成功，接下来我们就需要定位我们需要的数据

![markdown17569167-2cae166851f17174.webp.jpg](http://pxpfco2u1.bkt.clouddn.com/markdown17569167-2cae166851f17174.webp.jpg){:width="100%" align=center}



#### 定位内容

在刚刚获取的网页内容中，看到了我们需要的内容

*   ```bdc```代表学习单词情况

*   ```listen```代表学习听力情况

*   ```sentence```代表学习句子情况

#### 定位开始和结束位置

我们发现，这些数据最开始的部分，是从```“stats”```开始的，到```“track_object_img”```结束

*   这里注意，选择离你要的内容近一点的定位目标

*   定位近，为后续字符串操作提供便利

*   定位太远了，就需要删减很多内容

那我们首先，先把从```“stats”```到```“track_object_img”```的内容提出来

```Python
find_data = re.findall("\"stats\".*?track_object_img" ,shanbay_data)
```

这里我们调用了re 模块来使用正则表达式

正则表达式：使用单个字符串来描述、匹配一系列符合某个句法规则的字符串

官方文档：[re — Regular expression operations](https://docs.python.org/3/library/re.html)

怎么定位到我们需要的内容？用search或者find来找

```Python
re.search() 
re.findall()  
```


具体内容怎么表达？用符号匹配

```Python
^      # 匹配字符串的开头
$      # 匹配字符串结尾
.      # 匹配任意字符
*      # 表示任意次（从0到无限）
+      # 表示至少一次或任意次数

[0-9]  # 从0至9共十个数字中的任意一个
[a-z]  # 从小写a到z，26个字母中的一个
[A-Z]  # 从大写A到Z，26个字母的一个

\s     # 用于匹配单个空格，包括tab键和换行符 
\S     #  用于匹配单个空格之外的所有字符 
\d     # 匹配0-9的数字 
\w     # 匹配字母、数字或下划线 
```

举例：我们前面说过，要把```“stats”```到```“track_object_img”```的内容提出来，我们就可以这么表达

```
re.findall("\"stats\".*?track_object_img" ,shanbay_data)
```

讲解一下这句代码：

1、 用findall找出所有从```“stats”```到```“track_object_img”```的内容

2、```\"stats\" ```（开始位置）```.```（匹配任意字符）```*```（任意次数）```track_object_img```（结束位置）

此处可能会有两个疑问：

- ```\"stats\"``` 为什么要```\"```，不直接```"```？

因为```"```在Python中有特殊作用（```"字符串"```，```"```是字符串的标志），所以我们用到```"```的时候，用```\"```来表示

- 代码中间那个```？```要来干嘛的？

是避免贪婪匹配。

贪婪匹配：我从A匹配到B，默认是从第一个A匹配到最后一个B

非贪婪匹配：第一个A匹配到第一个B

到这一步，我们就把所有我们需要的内容提取出来了，下面开始具体清洗提取我们要的数据。

------------


### 清洗数据

------------


```Python
find_data = re.findall("\"stats\".*?track_object_img" ,shanbay_data)
```
 
经过上一步，我们把所有需要的内容都保存在```find_data```中，```find_data```里面此时有20条数据，是我最近20天的打卡情况

![markdown17569167-dd44b6423ecddf74.webp.jpg](http://pxpfco2u1.bkt.clouddn.com/markdown17569167-dd44b6423ecddf74.webp.jpg){:width="100%" align=center}

我们仔细观察```find_data```数据，可以看到，打卡的内容是有规律的。

> "stats": {"sentence": {"num_today": 5, "used_time": 2.0}, "bdc": {"num_today": 26, "used_time": 5.0}, "listen": {"num_today": 11, "used_time": 14.0}}, "track_object_img"

所有的内容，都会有一个```num_today```和```used_time```。就是你今天学了多少，花了多少时间。这两个数据，就是我们想要的。开心，继续往下~

我需要一条一条把信息读出来，这就需要一个```for```循环

```Python
for data in find_data:       
        read = re.findall("\"read\":.*?}",data)
        if read == []:
           read = "{num_today\": 0, \"used_time\": 0.0}"
        
        listen = re.findall("\"listen\":.*?}",data)
        if listen == []:
            listen = "{num_today\": 0, \"used_time\": 0.0}"
        
        sentence = re.findall("\"sentence\":.*?}",data)
        if sentence == []:
            sentence = "{num_today\": 0, \"used_time\": 0.0}"
        
        bdc = re.findall("\"bdc\":.*?}",data)
        if bdc == []:
            bdc = "{num_today\": 0, \"used_time\": 0.0}"    
```

用```for```循环依次取读20条数据，提取里面的阅读```read```、听力```listen```、句子```sentence```、单词```bdc```数据

这里我们用一个```if```判断，如果```find_data```里面有这部分内容，就提取出来，如果没有（也就是我们没有学习这部分），我们就构造一段字符串```{num_today\": 0, \"used_time\": 0.0}```，把```num_today```和```used_time```设置为0，和其他内容统一起来

大家可以看到，我用了4个```re.findall```，把阅读```read```、听力```listen```、句子```sentence```、单词```bdc```数据取出来
以单词```bdc```为例，这时候提取的数据如下

![markdown17569167-e0d46d0a5933a3f0.webp.jpg](http://pxpfco2u1.bkt.clouddn.com/markdown17569167-e0d46d0a5933a3f0.webp.jpg){:width="100%" align=center}

怎么具体提取出```60```和```11.0 ```这两个数字呢？

```Python
bdc_num = re.findall(r"\d+\.?\d*",str(bdc))[0]
bdc_time = re.findall(r"\d+\.?\d*",str(bdc))[1]
```

还是用re正则化表达，用```\d```把所有数字提取出来，第一个数字赋值给```bdc_num ```，第二个数字赋值给```bdc_time ```

![markdown17569167-d438e0480396088e.webp.jpg](http://pxpfco2u1.bkt.clouddn.com/markdown17569167-d438e0480396088e.webp.jpg){:width="100%" align=center}

操作到这一步，所有的信息相当于都提取好了

下面我们来思考一个问题，统计时间怎么确定？

我想要统计最近一周的打卡情况

------------


### 设置时间

------------



```Python
import datetime  # 先把datetime这个模块导入进来
```

（1）怎么确定查卡时间？可以有两种操作方式

```Python
now = datetime.datetime.now()      # 输入查卡日期，默认是今天
now = datetime.date(2019,5,13)      # 输入查卡日期，自定义
```

（2）	怎么定义范围？我只想统计一周的数据

```Python
time2 = datetime.timedelta(days=8)  # 统计一个星期的数据
day_now = str(now).split(" ")[0]    # 把日期取出来，后面的几点几分就不要了
day_end = now - time2               # 计算统计结束的那天
```

（3） 获取网页中的打卡时间

```Python
# 获取打卡天数
    checkin_time = []
    num_checkin_days = []
    find_checkin = re.findall("\"checkin_time\".*?\"share_urls\"",shanbay_data) 
    for checkin in find_checkin:
        shanbey_time = checkin.split(",")[0]
        shanbey_days = checkin.split(",")[3]
        checkin_time.append(str(shanbey_time)[len("\"checkin_time\": \""):len("\"checkin_time\": \"")+10])
        num_checkin_days.append(str(shanbey_days)[len("\"num_checkin_days\": "):])
```

这里我们引入字符串的基本操作

```Python
str()         将数值转变为字符串
str[::1]      将字符串倒序
ord()         获取字符的整数表示
chr()         把编码转换为对应的字符
.join()       串联若干字符
.format()     可以将字符串中的部分字符变成变量

.upper()      将字符串中的所有英文字母变成大写
.lower()      将字符串中的所有英文字母变成小写
.swapcase()   将字符串中的所有英文字母大小写互换
.title()      所有单词首字母大写

.split()      切割字符串
.strip()      删去字符串开头和结尾的空格或字符
.lsrtip()     与.strip()功能相似，从字符串左侧开始，遇到第一个不需要移除的字符则停止

.replace()    替换字符串中的某一部分
b.find(a)     返回字符串 a 在字符串 b中第一次出现所在的索引位置
```

我们先来看，用```find_all```把打卡时间这部分的数据提取出来，同样是20条数据，包含了打卡的具体时间

![markdown17569167-2cb3e184bed6a84d.webp.jpg](http://pxpfco2u1.bkt.clouddn.com/markdown17569167-2cb3e184bed6a84d.webp.jpg){:width="100%" align=center}

打开其中一条数据，发现我们要的时间```2019-05-22```和打卡天数```538```在不同的位置

![markdown17569167-d3c62e79859d71a7.webp.jpg](http://pxpfco2u1.bkt.clouddn.com/markdown17569167-d3c62e79859d71a7.webp.jpg){:width="100%" align=center}

这里我们用```.split()```，先根据逗号，把这个字符串分开

```Python
shanbey_time = checkin.split(",")[0] 
shanbey_days = checkin.split(",")[3]
```

![markdown17569167-fc1a62d91a81e3ae.webp.jpg](http://pxpfco2u1.bkt.clouddn.com/markdown17569167-fc1a62d91a81e3ae.webp.jpg){:width="100%" align=center}

然后截取字符串，用```len()```统计前面那些字符的个数，这些字符就不要了

用```append```依次把内容加上去

```Python
checkin_time.append(str(shanbey_time)[len("\"checkin_time\": \""):len("\"checkin_time\": \"")+10])
num_checkin_days.append(str(shanbey_days)[len("\"num_checkin_days\": "):])
```


![markdown17569167-87eb564f758fa069.webp.jpg](http://pxpfco2u1.bkt.clouddn.com/markdown17569167-87eb564f758fa069.webp.jpg){:width="100%" align=center}

![markdown17569167-55e1b8bfac6165ba.webp.jpg](http://pxpfco2u1.bkt.clouddn.com/markdown17569167-55e1b8bfac6165ba.webp.jpg){:width="100%" align=center}

这时候，我们只要再上一个```if``` 判断一下，统计从昨天开始的打卡记录

```Python
 if checkin_time[count] >= day_now:
            count += 1
        elif checkin_time[count] > day_end:            
            # 统计总时间和各项时间
            time_total = float(read_time)+float(listen_time)+float(bdc_time)+float(sentence_time);
            time_read = time_read+float(read_time);
            time_listen = time_listen+float(listen_time);
            time_bdc = time_bdc+float(bdc_time);
            time_sentence = time_sentence+float(sentence_time);  
            
            # 统计各项数目累计
            count_read = count_read+float(read_num)
            count_listen = count_listen+float(listen_num)
            count_bdc = count_bdc+float(bdc_num)
            count_sentence = count_sentence+float(sentence_num)
            
            # 输出一周每日打卡情况
            print("{},打卡{}天：阅读{}篇,听力{}句,单词{}个,炼句{}句,学习时间{}分钟".format
			(checkin_time[count],num_checkin_days[count],read_num,listen_num,bdc_num,sentence_num,time_total))
            count += 1
        else:
            break
```

最后输出结果

```Python
print("单词:{}分钟，总计{}个".format(time_bdc,count_bdc))print("阅读:{}分钟，总计{}篇".format(time_read,count_read))
print("炼句:{}分钟，总计{}句".format(time_sentence,count_sentence))
print("听力:{}分钟，总计{}句".format(time_listen,count_listen))
print('\n') 
print("打卡时长:{}分钟".format(time_read+time_sentence+time_bdc+time_listen))
```
 <br />
![markdown17569167-598df90ac445bec3.webp.jpg](http://pxpfco2u1.bkt.clouddn.com/markdown17569167-598df90ac445bec3.webp.jpg){:width="100%" align=center}

------------


###  保存数据

------------


在获取自己的打卡情况之后，我觉得这种都输在屏幕上的内容，很难整理，不适合小组打卡。我需要它能自动保存到Excel
这里要注意，用到Excel相关功能的时候，要导入相关库`pip install xlwt`

```Python
import xlwt  # 把Excel输出模块加进来

# 定义保存Excel的位置
workbook = xlwt.Workbook()  #定义workbook
sheet = workbook.add_sheet('本周打卡')  #添加sheet
head = ['打卡', '单词', '阅读', '炼句', '听力', '学习时间']    #表头
for h in range(len(head)):
    sheet.write(0, h, head[h])    #把表头写到Excel里面去
    
# 把内容保存到Excel
sheet.write(i, 0, checkin_time[count])  # 第i行，第1列
sheet.write(i, 1, bdc_num)  # 第i行，第2列
sheet.write(i, 2, read_num)  # 第i行，第3列
sheet.write(i, 3, sentence_num)  # 第i行，第4列
sheet.write(i, 4, listen_num)  # 第i行，第5列
sheet.write(i, 5, time_total)  # 第i行，第6列

# 保存Excel表
workbook.save('C:/Users/Administrator/Desktop/扇贝打卡.xls')
print('写入excel成功')
print("文件位置：")
print("C:/Users/Administrator/Desktop/扇贝打卡.xls")
```

此时程序运行效果如下：

![markdown17569167-223a054d5353b977.jpg](http://pxpfco2u1.bkt.clouddn.com/markdown17569167-223a054d5353b977.jpg){:width="100%" align=center}

接着，小组有这么多ID，每次改一改，我都要手动输，那太麻烦了。

我需要一个代码，把ID自动导入程序




```python
# 从txt导入数据
ID_total_input = open('C:/Users/Administrator/Desktop/user.txt')
ID_total = ID_total_input.read()
ID_total = ID_total.split("\n")  # 如果输入多个ID，用“\n”分开
```

自动读取ID、查卡、保存到EXCEL

![markdown17569167-6f794b6790ed1e44.jpg](http://pxpfco2u1.bkt.clouddn.com/markdown17569167-6f794b6790ed1e44.jpg){:width="100%" align=center}

最后，思考一下，需要导出小组打卡的哪些数据内容，调整代码

小组打卡输出EXCEL情况如下：(昵称和ID做了打码处理)

![markdown17569167-84e9b840e28e1d8b.jpg](http://pxpfco2u1.bkt.clouddn.com/markdown17569167-84e9b840e28e1d8b.jpg){:width="100%" align=center}

------------


### 完整代码

------------


Python爬虫：[获取扇贝打卡信息](http://www.zhaojingyi0126.com/post/7/)

Python爬虫：[将爬虫结果保存到Excel](http://www.zhaojingyi0126.com/post/16/)

Python爬虫：[从TXT导入数据](http://www.zhaojingyi0126.com/post/17/)



------------


### Python远不止爬虫

------------



坦白说，在学习编程40天的时候，我能写出小组查卡代码，我是非常欣喜和嘚瑟的。我还去小组技术群和扇贝编程群，要求大家表扬我，哈哈。

爬虫很有用。我日常是科研狗，整理课题相关的6000多篇文献，去年我用了半个月，今年我用了2个小时写了个代码。

但是Python的内容远不止爬虫。

我们小组的组员，因为工作需要，需要将几百页PDF文档中的内容转成EXCEL表格，Python几十行代码搞定

```python
import pdfplumber
import xlwt

# 定义保存Excel的位置
workbook = xlwt.Workbook()  #定义workbook
sheet = workbook.add_sheet('Sheet1')  #添加sheet
i = 0 # Excel起始位置

path = input("请输入PDF文件位置：")    
#path = "aaaaaa.PDF"  # 导入PDF路径
pdf = pdfplumber.open(path)
print('\n')
print('开始读取数据')
print('\n')
for page in pdf.pages:
    # 获取当前页面的全部文本信息，包括表格中的文字
    # print(page.extract_text())                     
    for table in page.extract_tables():
        # print(table)
        for row in table:            
            print(row)
            for j in range(len(row)):
                sheet.write(i, j, row[j])
            i += 1
        print('---------- 分割线 ----------')

pdf.close()

# 保存Excel表
workbook.save('C:/Users/Administrator/Desktop/PDFresult.xls')
print('\n')
print('写入excel成功')
print('保存位置：')
print('C:/Users/Administrator/Desktop/PDFresult.xls')
print('\n')
input('PDF取读完毕，按任意键退出')
```
 另外，做PPT图表总是很丑？

![markdown17569167-b0dcf9d3d4f58786.webp.jpg](http://pxpfco2u1.bkt.clouddn.com/markdown17569167-b0dcf9d3d4f58786.webp.jpg){:width="100%" align=center}

Python这么多好看的图表，只要改改参数，你就能拥有。不考虑一下？

[数据可视化：pygal](https://www.jianshu.com/p/19a4b050fb03)

Python其他我未知的功能，等我学习了再来和大家分享。

### 最后

以上内容都只是入门代码，爬虫代码中也不涉及编写函数、账号密码登入等内容。我的编程课程还没有结束，学习永无止境。

为什么要写下这个帖子，来和大家一起分享代码？

因为我们组员Grit说过：

> Learning by doing. Learning by teaching.

和大家共勉，一起学习