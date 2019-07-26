# -*- coding: utf-8 -*-
import json
import os
import re
import time
import os
import json
from scrapy.selector import Selector
import requests

url = 'https://m.dianping.com/shop/92040324'
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en',
    # 'DNT': '1',
    'Host': 'm.dianping.com',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Mobile Safari/537.36'
}
current_path = os.path.dirname(__file__)
parent_path = os.path.dirname(os.path.dirname(current_path))
path = './data/search.add.2'
count = 0
session  = requests.session()
import random

while 1:
    try:
        time.sleep(2)
        session = requests.session()
        session.get('https://m.dianping.com/', headers=headers, timeout=3)
        print('retrying....')
        break
    except Exception as e:
        print(e)
        time.sleep(2)
        continue

with open('./data/detail.{}'.format(str(random.random())[-4:]),'w') as fw:
    with open(path, 'r') as f:
        line = f.readline()
        while line:
            if count < 28774:
                count+=1
                print(count)
                line = f.readline()
                continue
            try:
                data = json.loads(line)
            except Exception:
                continue
            shop_id = data['shop_id']
            temp = re.sub('(p2.*)$', '', data['url'])
            page = re.findall('(p\d+)', data['url'])
            if page:
                temp += page[-1]
            headers['Referer'] = 'http://m.dianping.com/alashan/ch10/g134r3592'
            # shop_id = '100091635'
            url = 'http://www.dianping.com/shop/{}'.format(shop_id)
            print(url)
            while 1:
                try:
                    r = session.get(url, headers=headers,timeout=5)
                except Exception as e:
                    print(e)
                    time.sleep(2)
                    continue
                break
            if  r.url != url:
                while 1:
                    try:
                        time.sleep(2)
                        session = requests.session()
                        session.get('https://m.dianping.com/', headers=headers,timeout=3)
                        print('retrying....',shop_id)
                        break
                    except Exception as e:
                        print(e)
                        time.sleep(2)
                        continue
                line = line
                continue
            print(r.status_code)
            html = r.text
            print(r.url)
            tel = Selector(text=html).css('.tel::attr(href)').extract()
            print(tel)
            result = {
                'phone_num' : [i.replace('tel:', '') for i in tel],
                'shop_name' : data['shop_name'] , # 名称，
                'city' : data['city'] , # 城市，
                'district' : data['district'] , # 区，
                'map_poi' :data['map_poi'],
                'shop_id' : data['shop_id'],
                'rank_star' :data['rank_star'],
                'region': data['region'] , # 商圈，
                'area' :data['area'],
                'address': data['address'] , # 地址，
                'type' : data['type'],  # 行业，
                'review_num' : data['review_num'],
            }
            print(result)
            fw.write(json.dumps(result,ensure_ascii=False))
            fw.write('\n')
            fw.flush()
            time.sleep(0.5)
            line = f.readline()
