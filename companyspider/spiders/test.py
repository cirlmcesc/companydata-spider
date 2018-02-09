# -*- coding: utf-8 -*-

import re
import scrapy
from scrapy.http import Request

class TestSpider(scrapy.Spider):
    name = 'test'
    allowed_domains = ['test.com']
    start_urls = ['http://test.com/']
    item_dict = {
        u'地点': 'location',
        u'性质': 'nature',
        u'规模': 'scale',
        u'行业': 'industry',
        u'地址': 'address',
        u'电话': 'telephone',
        u'介绍': 'description',
        u'网站': 'homepage',
    }

    def start_requests(self):
        url = "http://company.zhaopin.com/%E6%B7%B1%E5%9C%B3%E5%B8%82%E9%97%A8%E8%80%81%E7%88%B7%E7%A7%91%E6%8A%80%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8_CC273091518.htm"
        yield Request(url)

    def parse(self, response):
        scrapy.shell.inspect_response(response, self)
        # company_item = {}

        # for tr in response.xpath('//table[@class="comTinyDes"]/tr'):
        #     tr_text = tr.xpath('td/span/text()').extract()
        #     field, value = tr_text[0], tr_text[1]

        #     for zh_field in self.item_dict:
        #         if zh_field in field:
        #             company_item[self.item_dict.get(zh_field)] = value

        # description = response.xpath('//div[@class="company-content"]').extract()
        # description = re.sub(r'</?\w+[^>]*>', '', description[0]) # 剔除html标签
        # company_item['description'] = description.strip()
        # scrapy.log.msg(company_item, level=scrapy.log.INFO)

