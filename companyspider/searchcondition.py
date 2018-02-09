# -*- coding: utf-8 -*-

import re


industries = (
    u"网络游戏",
    u"耐用消费品",
    u"零售/批发",
    u"媒体/出版/影视/文化传播",
    u"旅游/度假",
    u"家居/室内设计/装饰装潢",
    u"快速消费品",
    u"基金/证券/期货/投资",
    u"教育/培训/院校",
)

cities = (
    u"上海",
    u"北京",
    u"广州",
    u"杭州",
    u"深圳",
)

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

maxpage = 90

company_min_scale = 100

company_scale_weight = {
    100: 1,
    500: 2,
    1000: 3,
}

weight_standard = (
    'scale',
    'url',
    'homepage',
    'address',
)

def scale_weighting(scale):
    weight = 0

    if not scale:
        return weight

    scale = int(
        re.findall(r'\d+\-\d+', scale)[0].split('-')[0]
    ) if '-' in scale else int(
        re.findall(r'\d+', scale)[0])

    if scale >= company_min_scale:
        for scale_weight in company_scale_weight:
            if scale >= scale_weight:
                weight += company_scale_weight.get(scale_weight)

    return weight

def url_weighting(url):
    weight = 0

    if 'xiaoyuan' in url:
        weight += 7
    elif 'special' in url:
        weight += 10

    return weight

def weighting(company, standard=weight_standard):
    benchmark = 0

    if 'scale' in standard:
        benchmark += scale_weighting(company.get('scale'))

    if 'url' in standard:
        benchmark += url_weighting(company.get('url'))

    if 'homepage' in standard:
        benchmark += 1 if company.get('homepage', False) else 0

    if 'address' in standard:
        benchmark += 1 if company.get('address', False) else 0

    company['weight'] = benchmark

