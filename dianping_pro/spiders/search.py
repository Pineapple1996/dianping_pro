# -*- coding: utf-8 -*-
import json
import re

import scrapy
import scrapy
from dianping_pro.items import DianpingProItem
import os
from dianping_pro.config import HEADERS
from dianping_pro.funcs import decode_poi,convert_api,filter_tags

class SpiderSpider(scrapy.Spider):
    name = 'search'
    allowed_domains = ['www.dianping.com']
    start_urls = ['http://www.dianping.com/']
    custom_settings = {
        'LOG_LEVEL' : 'WARNING',
        'CONCURRENT_REQUESTS_PER_DOMAIN' : 1,
        'CONCURRENT_REQUESTS_PER_IP' :  1,
        'RANDOMIZE_DOWNLOAD_DELAY': True
    }

    def start_requests(self):
        self.convert_dict = {}
        current_path = os.path.dirname(__file__)
        parent_path = os.path.dirname(current_path)
        path = '{}/city.json'.format(parent_path)
        with open(path,'r') as f:
            lines = f.readlines()
            for i in lines:
                try:
                    data = json.loads(i)
                except Exception:
                    continue
                city = data['city']
                print(city)
                domain = data['demain']
                type_l = ['/ch10/g134','/ch10/g132']

                for m in type_l:
                    url = 'http://'+domain+m
                    print(url)
                    HEADERS['Referer'] = url
                    yield scrapy.Request(
                        url=url,
                        headers=HEADERS,
                        meta={'city':city},
                        callback=self.parse_distric
                    )


    def parse_distric(self, response):
        district = response.css('#region-nav a')
        for i in district:
            name = i.css('a::attr(data-click-title)').extract()[0]
            link = i.css('a::attr(href)').extract()[0]
            HEADERS['Referer'] = link
            yield scrapy.Request(
                url=link,
                headers=HEADERS,
                meta={'city': response.meta['city'],'district':name},
                callback=self.parse_area
            )


    def parse_area(self,response):
        area = response.css('#region-nav-sub a')
        for i in area:
            if i=='不限':
                continue
            name = i.css('a span::text').extract()[0]
            link = i.css('a::attr(href)').extract()[0]
            print(name,link)
            HEADERS['Referer'] = link
            yield scrapy.Request(
                url=link,
                headers=HEADERS,
                meta={'city': response.meta['city'], 'district': response.meta['district'],'area':name,'page':1,'link':link},
                callback=self.parse
            )


    def parse(self, response):
        shop_list = response.css('.shop-list >ul >li')
        item = DianpingProItem()
        item['url'] = response.url
        if not re.findall(
            r'href="(//s3plus.*?svgtextcss.*\.css)"', response.text):
            link = response.meta['link']
            HEADERS['Referer'] = link
            yield scrapy.Request(
                url=link,
                headers=HEADERS,
                meta={'city': response.meta['city'], 'district': response.meta['district'], 'area': response.meta['area'], 'page': 1,
                      'link': link},
                callback=self.parse
            )
            return
        self.svg_css_url = re.findall(
            r'href="(//s3plus.*?svgtextcss.*\.css)"', response.text)[0]
        # print(self.svg_css_url)
        for li in shop_list:
            if not li:
                continue
            shop_id = li.css('.tit >a[data-click-name=shop_title_click]::attr(data-shopid)').extract()[0]
            shop_name = li.css('.tit >a h4::text').extract()[0]
            rank_star = li.css(
                '.comment .sml-rank-stars::attr(title)').extract()[0]
            map_poi = li.css('.J_operate .o-map::attr(data-poi)').extract()[0]
            map_poi = decode_poi(map_poi)
            review_num_span = li.css(
                '.comment  .review-num .shopNum').extract()
            review_num = ''
            for span in review_num_span:
                tag_name = re.findall('class="(\w+)"',span)[0]
                text = re.findall('>(.*)<',span)[0]
                if text in self.convert_dict:
                    num = self.convert_dict[text]
                else:
                    num = convert_api(text, tag_name, self.svg_css_url)
                    self.convert_dict[text] = num
                review_num +=num

            print(review_num)
            address = li.css(
                '.J_operate .o-map::attr(data-address)').extract()[0]

            region_tag_text = li.css(
                '.tag-addr a[data-click-name=shop_tag_region_click] .tag').extract()[0]
            tag_taste_text = li.css(
                '.tag-addr a[data-click-name=shop_tag_cate_click] .tag').extract()[0]
            tag_taste_list = li.css(
                '.tag-addr a[data-click-name=shop_tag_cate_click] .tag .tagName').extract()
            tag_region_list = li.css(
                '.tag-addr a[data-click-name=shop_tag_region_click] .tag .tagName').extract()


            for span in tag_taste_list:
                tag_name = re.findall('class="(\w+)"', span)[0]
                text = re.findall('>(.*)<', span)[0]
                if text in self.convert_dict:
                    convert_text = self.convert_dict[text]
                else:
                    convert_text = convert_api(text, tag_name, self.svg_css_url)
                    self.convert_dict[text] = convert_text
                tag_taste_text = tag_taste_text.replace(span,convert_text)
            for span in tag_region_list:
                tag_name = re.findall('class="(\w+)"', span)[0]
                text = re.findall('>(.*)<', span)[0]
                if text in self.convert_dict:
                    convert_text = self.convert_dict[text]
                else:
                    convert_text = convert_api(text, tag_name, self.svg_css_url)
                    self.convert_dict[text] = convert_text
                region_tag_text = region_tag_text.replace(span,convert_text)

            region = filter_tags(region_tag_text)
            type = filter_tags(tag_taste_text)


            item['shop_name'] = shop_name  # 名称，
            item['city'] = response.meta['city']  # 城市，
            item['district'] = response.meta['district']  # 区，
            item['map_poi'] = map_poi
            item['shop_id'] = shop_id
            item['rank_star'] = rank_star
            item['region'] = region # 商圈，
            item['area'] = response.meta['area']
            item['address'] = address  # 地址，
            item['type'] = type  # 行业，
            item['review_num'] = review_num

            print(item)
            yield item
            next_page = response.css('.page .next::attr(href)').extract()
            page = response.meta['page']
            if next_page:
                page+=1
                url = response.url+'p{}'.format(page)
                HEADERS['Referer'] = url
                yield scrapy.Request(
                    url=url,
                    headers=HEADERS,
                    meta={'city': response.meta['city'], 'district': response.meta['district'], 'area': response.meta['area'],'page':page,'link':response.meta['link']},
                    callback=self.parse
                )
