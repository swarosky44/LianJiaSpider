# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LianjiaprojectItem(scrapy.Item):
    # 标签
    title = scrapy.Field()
    # 小区
    community = scrapy.Field()
    # 户型
    model = scrapy.Field()
    # 面积
    area = scrapy.Field()
    # 观看人数
    watch_num = scrapy.Field()
    # 发布时间
    time = scrapy.Field()
    # 价格
    price = scrapy.Field()
    # 详情链接
    link = scrapy.Field()
    # 经纬度
    latitude = scrapy.Field()
    longitude = scrapy.Field()
    # 城区
    city = scrapy.Field()
