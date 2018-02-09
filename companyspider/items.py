# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CompanyInfomationItem(scrapy.Item):
    url = scrapy.Field() #所在招聘网站地址
    name = scrapy.Field() #公司名称
    homepage = scrapy.Field() #公司主页
    address = scrapy.Field() #公司地址
    telephone = scrapy.Field() #公司电话
    scale = scrapy.Field() #公司规模
    location = scrapy.Field() #公司位置
    nature = scrapy.Field() #公司性质
    industry = scrapy.Field() #公司行业
    description = scrapy.Field() #公司介绍
    contacter = scrapy.Field() #联系人
    weight = scrapy.Field() # 权重