# coding=utf-8
import json
import time
from datetime import datetime
from lxml import etree
import scrapy
from university.items import UniversityItem
from scrapy.conf import settings


class University(scrapy.Spider):
    """
    (英国、新西兰、法国)大学爬虫
    """
    name = 'England'
    l1 = ['塞浦路斯', '丹麦', '英国', '马来西亚', '新西兰', '波兰', 
    '埃及', '匈牙利', '拉脱维亚（特殊）', '以色列', '卢森堡']
    need = ['中国香港', '新加坡', '俄罗斯', '德国', '', '',]



    def __init__(self, *args, **kwargs):
        # self.spider_list = ['英国']
        self.spider_list = ['法国']

    def start_requests(self):
        """初始请求"""
        url = 'http://www.jsj.edu.cn/n1/12018.shtml'
        yield scrapy.Request(url, callback=self.country_parse)

    def country_parse(self, response):
        """国家解析"""
        item = UniversityItem()
        country_name_list = response.xpath('//div[@class="scList"]//a/text()').extract()
        country_link_list = response.xpath('//div[@class="scList"]//a/@href').extract()
        for i in range(len(country_link_list)):
            if country_name_list[i].strip() not in self.spider_list:
                continue
            item['country_name'] = country_name_list[i].strip()
            item['country_link'] = country_link_list[i].strip()
            yield scrapy.Request(item['country_link'], callback=self.university_parse, meta=item)
            

    def university_parse(self, response):
        print('---解析---')
        uni_obj = response.xpath("//div[@class='gwList']")
        for i in range(len(uni_obj)):
            res = uni_obj[i].xpath('./p/text()').extract()
            response.meta['campus'] = res[0].split('：')[-1].strip()
            response.meta['native_uni_name'] = response.meta['campus'].split('(')[0].strip()
            response.meta['chinese_uni_name'] = res[1].split('：')[-1].strip()
            response.meta['website'] = res[2].split('：')[-1].strip()
            response.meta['remarks'] = res[-1].split('：')[-1].strip()
            response.meta['last_update_date'] = datetime.now()
            yield response.meta


        
