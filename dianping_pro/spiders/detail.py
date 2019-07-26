# -*- coding: utf-8 -*-

import json
import re
import scrapy
from dianping_pro.items import DianpingProItem
import os
from dianping_pro.config import HEADERS
from dianping_pro.funcs import decode_poi,convert_api,filter_tags,get_dianping_cookies

class SpiderSpider(scrapy.Spider):
    name = 'detail'
    allowed_domains = ['www.dianping.com']
    start_urls = ['http://www.dianping.com/']
    custom_settings = {
        'CONCURRENT_REQUESTS_PER_IP': 1,
        'DOWNLOAD_DELAY': 1,
        'CONCURRENT_REQUESTS': 1,
        'CONCURRENT_REQUESTS_PER_DOMAIN' : 2
    }
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en',
        # 'DNT': '1',
        'Host': 'm.dianping.com',
        'Cookie': '__mta=107255229.1552638186944.1554175700124.1554180161222.11; _lxsdk_cuid=1696a7f19f5c8-04c8109b68604a-3d750e5e-1fa400-1696a7f19f5c8; _lxsdk=1696a7f19f5c8-04c8109b68604a-3d750e5e-1fa400-1696a7f19f5c8; _hc.v=a38ab82c-6898-cf85-3d30-6e9edee30fee.1552269909; aburl=1; switchcityflashtoast=1; Hm_lvt_e6f449471d3527d58c46e24efb4c343e=1552872515,1552872559; Hm_lvt_4c4fc10949f0d691f3a2cc4ca5065397=1552898022; s_ViewType=10; wedchatguest=g1035148039491148; _adwp=169583271.5237670369.1553769648.1553769648.1553769648.1; _adwr=169583271%230; cye=chengdu; m_flash2=1; __utma=205923334.1719018507.1553849399.1553849399.1553849399.1; __utmc=205923334; __utmz=205923334.1553849399.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); logan_custom_report=; cy=8; Hm_lvt_dbeeb675516927da776beeb1d9802bd4=1552637225,1553497718,1553499861,1554109875; dp_pwa_v_=1672865b011de2e1f16a640b5af838452230dcb0; Hm_lpvt_dbeeb675516927da776beeb1d9802bd4=1554180196; PHOENIX_ID=0a4f3576-169dc9e7239-b30a9; _tr.u=FKj1roXQrl1Des1D; _tr.s=jHjqLDUd8fJcexE5; msource=default; source=m_browser_test_22; cityid=1;  _lxsdk_s=169dcc509fb-f4b-d-531%7C%7C1',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Mobile Safari/537.36'
    }
    def start_requests(self):
        current_path = os.path.dirname(__file__)
        parent_path = os.path.dirname(os.path.dirname(current_path))
        path = '{}/data/search.1'.format(parent_path)
        count = 0
        with open(path, 'r') as f:
            line = f.readline()
            while line:
                # if count < 11500:
                #     count+=1
                #     print(count)
                #     line = f.readline()
                #     continue

                try:
                    data = json.loads(line)
                except Exception:
                    continue
                shop_id = data['shop_id']
                url = 'https://m.dianping.com/shop/{}'.format(shop_id)
                temp = re.sub('(p2.*)$', '', data['url'])
                page = re.findall('(p\d+)', data['url'])
                if page:
                    temp += page[-1]
                # HEADERS['Referer'] = None
                print(url)
                yield scrapy.Request(
                    url=url,
                    headers=HEADERS,
                    meta={'data':data,'handle_httpstatus_list': [302],'url':url},
                    callback=self.parse,
                    dont_filter=True,
                    cookies={'default_ab':'shop%3AA%3A5','msource':'default'}
                )
                line = f.readline()

    def parse(self,response):
        print(response.status)
        if response.status == 302:
            print('retrying')
            data=response.meta['data']
            temp = re.sub('(p2.*)$', '', data['url'])
            page = re.findall('(p\d+)', data['url'])
            if page:
                temp += page[-1]
            HEADERS['Referer'] = ''
            yield scrapy.Request(
                url=response.meta['url'],
                headers=HEADERS,
                meta={'data': response.meta['data'], 'handle_httpstatus_list': [302],'url':response.meta['url']},
                callback=self.parse,
                dont_filter=True,
                cookies={'default_ab':'shop%3AA%3A5','msource':'default'}
                # cookies=get_dianping_cookies()
            )
            return
        item = DianpingProItem()
        data = response.meta['data']

        tel = response.css('.tel::attr(href)').extract()
        item['phone_num'] = [i.replace('tel:','')for i in tel]
        item['shop_name'] = data['shop_name']  # 名称，
        item['city'] = data['city']  # 城市，
        item['district'] = data['district']  # 区，
        item['map_poi'] = data['map_poi']
        item['shop_id'] = data['shop_id']
        item['rank_star'] = data['rank_star']
        item['region'] = data['region']  # 商圈，
        item['area'] = data['area']
        item['address'] = data['address']  # 地址，
        item['type'] = data['type']  # 行业，
        item['review_num'] = data['review_num']
        yield item
