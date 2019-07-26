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
### 3.反爬虫

