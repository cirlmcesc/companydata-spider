# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import scrapy
import time
from companyspider.items import CompanyInfomationItem
from companyspider.database.Pedoo import ORMModel
from companyspider import searchcondition

class Company(ORMModel):
    table_name = 'company_infomation'

class CompanyspiderPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, CompanyInfomationItem):
            if not Company.has('name', '=', item.get('scale')):
                searchcondition.weighting(item) # 计算权重
                company = Company(attributes=dict(item))
                company.save()

        return item