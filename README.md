## 大众点评爬虫
### 1.目录结构
```python
├── data      #数据文件夹
├── detail_spider_request.py   #详情更新单线程爬虫
├── dianping_pro      
│   ├── city.json
│   ├── config.py
│   ├── funcs.py         #附加函数
│   ├── get_all_cities.py  #获取所有城市节点脚本
│   ├── __init__.py
│   ├── items.py
│   ├── middlewares.py
│   ├── pipelines.py
│   ├── settings.py
│   └── spiders #爬虫文件夹
│       ├── detail.py
│       ├── __init__.py
│       └── search.py
├── README.md
├── scrapy.cfg
├── start_detail.py   #启动程序
└── start_search.py   #scrapy 启动
```

### 2.程序入口
```python
python3 start_search.py #启动搜索页面爬虫
python3 start_detail.py #启动详情页面爬虫（由于点评策略更新这个暂时失效）
python3 detail_spider_requests #启动详情页更新爬虫
```
### 3.反爬虫(19.7.10)
之前大众点评采用的css匹配svg转文字的办法来进行页面的字体加密,
前几天做大众点评的时候突然发现这个办法行不通了,
于是乎进行新的探索,发现这个新的套路和原来是差距不大的,
就是用woff文件来代替了之前的svg,woff肯定是更有难度的,
难点在于woff转换的xml内容里面不包含文字,大概是这样子的
![image](https://github.com/Pineapple1996/pics/blob/master/Screenshot%20from%202019-07-26%2016-29-00.png?raw=true)

但是他的对应的中文字符呢?我们尝试打开.woff文件看看
![image](https://github.com/Pineapple1996/pics/blob/master/Screenshot%20from%202019-07-26%2016-37-05.png?raw=true)
啧啧啧～～～
![image](http://www.gaoxiaogif.com/d/file/201807/8744497c1a6fbfcc6f907c7e0deab626.gif)
这就有点意思了，这不是能对应上么，可是这么多文字不能拿下来啊！
我采取的办法就是硬刚了,然后在过程中我才发现都是泪
<img src="http://img.mp.itc.cn/upload/20170317/c7e62fde63294fc889a7e345a71ad0a1_th.jpeg" width = "200" height = "200" alt="图片名称" align=center />
