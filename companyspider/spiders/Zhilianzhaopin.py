# -*- coding: utf-8 -*-

import scrapy
import random
import re
import urllib
import companyspider.searchcondition as searchcondition
from scrapy.http import Request
from scrapy import log
from companyspider.items import CompanyInfomationItem


def split_str(string, default=''):
    try:
        return string.split(u'：')[1]
    except IndexError:
        return default

class ZhilianzhaopinSpider(scrapy.Spider):
    name = 'Zhilianzhaopin'
    allowed_domains = ['zhaopin.com']
    start_urls = ['https://www.zhaopin.com/']
    search_url = "http://sou.zhaopin.com/jobs/searchresult.ashx"
    companyinfomation_url = "company.zhaopin.com"
    xiaozhao_url = "xiaoyuan.zhaopin.com"

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url, callback=self.parse_index_page, meta={'PhantomJS': True})

    def shell_debug(self, response):
        """ debug dom-tree in shell """
        scrapy.shell.inspect_response(response, self)

    def log_debug(self, msg, data, level=log.WARNING):
        """ 错误输出调试 """
        log.msg(u'|```````````````` %s ````````````````|' % msg, level=level)

        if isinstance(data, list):
            for a in data:
                log.msg(a, level=level)
        else:
            log.msg(data, level=level)

        log.msg('|________________ END ________________|', level=level)

    def parse_index_page(self, response):
        """ 主页 """
        for label in response.xpath('//label'):
            industry = label.xpath('text()').extract()[0]

            if industry in searchcondition.industries:
                for city in searchcondition.cities:
                    url = self.search_url + "?in=%s&jl=%s&sm=1&p=1" % (
                        label.xpath('input/@value').extract()[0], city)
                    yield Request(url, callback=self.parse_search_page,
                                  meta={'industry': industry})

    def parse_search_page(self, response):
        """ 处理条件搜索页面 """
        company_name = []

        for unit in response.xpath('//div[@class="newlist_detail newlist"]'):
            company_name_li = unit.xpath('div/ul/li[contains(@class, "gsmc")]')[0]
            company_detail_li = unit.xpath('div/ul/li[contains(@class, "newlist_deatil_two")]')[0]
            company = {'name': company_name_li.xpath('a/text()').extract()[0],
                       'url': company_name_li.xpath('a/@href').extract()[0],
                       'industry': response.meta.get('industry')}

            if not company.get('url', False):
                continue
            elif 'redirecturl' in company.get('url'):
                redirecturl = company.get('url').split('url=')
                company['url'] = urllib.unquote(redirecturl[1])

            for spanstr in company_detail_li.xpath('span/text()').extract():
                if u'地点' in spanstr:
                    company['location'] = split_str(spanstr)
                elif u'性质' in spanstr:
                    company['nature'] = split_str(spanstr)
                elif u'规模' in spanstr:
                    company['scale'] = split_str(spanstr)

            searchcondition.weighting(company, standard=['scale'])

            if int(company['weight']) > 0 and not company.get('name') in company_name:
                company_name.append(company.get('name'))
                yield Request(company.get('url'), meta={'company_detail': company},
                            callback=self.parse_companyinfomation_page)

        next_page_url = response.xpath(
            '//div[@class="pagesDown"]/ul/li[@class="pagesDown-pos"]/a/@href').extract()

        if next_page_url:
            yield Request(next_page_url[0], callback=self.parse_search_page,
                          meta={'industry': response.meta.get('industry')})

    def parse_companyinfomation_page(self, response):
        """ 处理公司详情页 """
        company_item = CompanyInfomationItem(response.meta.get('company_detail'))

        if response.xpath('//div') and self.companyinfomation_url in response.url: # 标准页面
            for tr in response.xpath('//table[@class="comTinyDes"]/tr'):
                tr_text = tr.xpath('td/span/text()').extract()

                if u'性质' in tr_text[0] and not company_item.get('nature'):
                    company_item['nature'] = tr_text[1] if len(tr_text) > 1 else ''
                elif u'规模' in tr_text[0]:
                    company_item['scale'] = tr_text[1] if len(tr_text) > 1 else ''
                elif u'行业' in tr_text[0]:
                    company_item['industry'] = tr_text[1] if len(tr_text) > 1 else ''
                elif u'网站' in tr_text[0] and not company_item.get('homepage'):
                    href = tr.xpath('td/span/a/@href').extract()
                    company_item['homepage'] = href[0] if len(href) else ''
                elif u'地址' in tr_text[0] and not company_item.get('address'):
                    address_text = tr_text[1] if len(tr_text) > 1 else ''
                    address = re.sub(r'</?\w+[^>]*>', '', address_text)
                    company_item['address'] = address.strip()

            description_text = response.xpath('//div[@class="company-content"]').extract()
            description = re.sub(r'</?\w+[^>]*>', '', description_text[0]) # 剔除html标签
            company_item['description'] = description.strip()
        elif self.xiaozhao_url in response.url: # 校招页面
            company_item = self.parse_xiaozhao_companinfomation_page(response, company_item)

        yield company_item

    def parse_xiaozhao_companinfomation_page(self, response, company_item):
        """ 处理校园招聘的公司信息页面 """
        company_guild = response.xpath('//div[@class="cCompanyGuild"]/p[@class="c9"]')[0]

        for detail in company_guild.xpath('span/text()').extract():
            if u'行业' in detail and not company_item.get('industry'):
                company_item['industry'] = detail.split(u'：')[1]
            elif u'规模' in detail and not company_item.get('scale'):
                company_item['industry'] = detail.split(u'：')[1]
            elif u'类型' in detail and not company_item.get('nature'):
                company_item['nature'] = detail.split(u'：')[1]

        for detail in response.xpath(
            '//div[@class="cRight r"]/div/div/p[contains(@class, "c9")]'
        ).extract():
            if detail and u'网址' in detail:
                selector = scrapy.selector.Selector(text=detail)
                company_item['homepage'] = selector.xpath('//a/@href').extract()[0]
            elif detail and not company_item.get('address'):
                company_item['address'] = detail.strip()

        return company_item