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
    (加拿大)大学爬虫
    """
    name = 'Canada'
    l1 = ['塞浦路斯', '丹麦', '英国', '马来西亚', '新西兰', '波兰', 
    '埃及', '匈牙利', '拉脱维亚（特殊）', '以色列', '卢森堡']

    @staticmethod
    def is_chinese(word):
        for ch in word:
            if '\u4e00' <= ch <= '\u9fff':
                return False
        return True

    def __init__(self, *args, **kwargs):
        self.spider_list = ['加拿大']

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
            yield scrapy.Request(item['country_link'], callback=self.nature_parse, meta=item)
    
    def nature_parse(self, response):
        """性质解析"""
        nature_list = response.xpath('//div[@id="Zoom"]/table//a/text()').extract()
        uni_list_link = response.xpath('//div[@id="Zoom"]/table//a/@href').extract()
        for i in range(len(nature_list)):
            response.meta['nature'] = nature_list[i].strip()
            response.meta['uni_list_link'] = 'http://www.jsj.edu.cn' + uni_list_link[i].strip()
            yield scrapy.Request(response.meta['uni_list_link'], callback=self.university_parse, meta=response.meta)
    
    def university_parse(self, response):
        uni_obj = response.xpath("//div[@id='Zoom']/p/text()").extract()
        for i in range(len(uni_obj)):
            if not uni_obj[i].strip():
                continue
            elif self.is_chinese(uni_obj[i]):
                response.meta['native_uni_name'] = response.meta['campus'] = uni_obj[i].strip()
                response.meta['last_update_date'] = datetime.now()
                yield response.meta
            elif not uni_obj[i].startswith('学校名称'):
                continue
            else:
                response.meta['native_uni_name'] = response.meta['campus'] = uni_obj[i].split('：')[-1].strip()
                response.meta['last_update_date'] = datetime.now()
                yield response.meta


        
