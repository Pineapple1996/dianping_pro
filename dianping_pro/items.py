# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html


import scrapy


class DianpingProItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    shop_name = scrapy.Field() # 名称，
    city = scrapy.Field()# 城市，
    district = scrapy.Field()# 区，
    region = scrapy.Field()#  商圈，
    address = scrapy.Field()# 地址，
    type = scrapy.Field()# 行业，
    phone_num = scrapy.Field()# 座机，手机号

    url = scrapy.Field()
    shop_id = scrapy.Field()
    area = scrapy.Field()
    rank_star = scrapy.Field()
    map_poi = scrapy.Field()
    # address = scrapy.Field()
    recommend_dish = scrapy.Field()
    comment_score = scrapy.Field()
    mean_price = scrapy.Field()
    review_num = scrapy.Field()
    tag_taste = scrapy.Field()
    tag_region = scrapy.Field()

