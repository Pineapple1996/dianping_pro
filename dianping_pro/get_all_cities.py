# -*- coding: utf-8 -*-
import json

from pyquery import PyQuery as pq
import requests

def get_page(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36'
    }
    r = requests.get(url=url,headers=headers)
    html_ = pq(r.text)
    div = html_('.main-citylist .letter-item')
    with open('city.json','w') as f:
        for i in div :
            d = pq(i)('.findHeight a')
            for m in d:
                name = pq(m).text()
                demain = pq(m).attr('href')
                print(name,demain)
                temp = {'city':name,'demain':demain.strip('//')}
                f.write(json.dumps(temp,ensure_ascii=False))
                f.write('\n')



if __name__ == '__main__':
    # url = 'https://www.dianping.com/citylist'
    # get_page(url)
    headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en',
            # 'Cookie': '_lxsdk_cuid=16bff1e13bb96-0b0b5ee1afd66c-1b29140e-1fa400-16bff1e13bcc8; _lxsdk=16bff1e13bb96-0b0b5ee1afd66c-1b29140e-1fa400-16bff1e13bcc8; _hc.v=f86821f2-9cf9-0cc8-f112-b02d1b7217d2.1563353290;_lxsdk_s=16c02bd6db5-e31-7c7-795%7C%7C47',
            'Referer': 'http://www.dianping.com/alashan/ch30/g132',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
        }

    r = requests.get(url ='http://www.dianping.com/alashan/ch30/g132',headers = headers)
    print(r.url)
    print(r.text)