# coding=utf-8
import json
import time
from datetime import datetime
import scrapy
from university.items import UniversityItem
from scrapy.conf import settings


class University(scrapy.Spider):
    """
    国外大学爬虫
    """
    name = 'America'

    @staticmethod
    def is_chinese(word):
        if word == ' Georgia Regents University（2012年1月8日由Augusta State University及':
            return True
        for ch in word:
            if '\u4e00' <= ch <= '\u9fff':
                return False
        return True

    def __init__(self, *args, **kwargs):
        pass

    def start_requests(self):
        """初始请求"""
        url = 'http://www.jsj.edu.cn/n1/12018.shtml'
        yield scrapy.Request(url, callback=self.country_parse)

    def country_parse(self, response):
        """国家解析"""
        item = UniversityItem()
        country_name_list = response.xpath('//div[@class="scList"]//a//text()').extract()
        country_link_list = response.xpath('//div[@class="scList"]//a/@href').extract()
        for i in range(len(country_link_list)):
            item['country_name'] = country_name_list[i].strip()
            item['country_link'] = country_link_list[i].strip()
            yield scrapy.Request(item['country_link'], callback=self.usa_list_parse, meta=item)
            break

    def usa_list_parse(self, response):
        """地区解析（美国）"""
        area_name_list = response.xpath('//*[@id="Zoom"]//a//text()').extract()
        area_link_list = response.xpath('//*[@id="Zoom"]//a/@href').extract()
        for i in range(len(area_link_list)):
            if area_name_list[i].strip() != 'Guam':
                continue
            response.meta['area_name'] = area_name_list[i].strip()
            response.meta['uni_list_link'] = 'http://www.jsj.edu.cn'+ area_link_list[i].strip()
            yield scrapy.Request(response.meta['uni_list_link'], callback=self.usa_parse, meta=response.meta)

    def usa_parse(self, response):
        if response.meta['area_name'] == 'Guam':
            campus_list = response.xpath('//*[@id="Zoom"]/text()').extract()
        else:
            campus_list = response.xpath('//*[@id="Zoom"]/p/text()').extract()
        for i in range(len(campus_list)):
            if not campus_list[i].strip() or not self.is_chinese(campus_list[i]):
                continue
            response.meta['native_uni_name'] = campus_list[i].split('(')[0].strip()
            response.meta['campus'] = campus_list[i].strip()
            response.meta['last_update_date'] = datetime.now()
            yield response.meta


        
