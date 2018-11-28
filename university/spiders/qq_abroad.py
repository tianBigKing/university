# coding=utf-8
import re
import json
import time
from datetime import datetime
from lxml import etree
import scrapy
from university.items import UniversityItem
from scrapy.conf import settings


class University(scrapy.Spider):
    """
    (腾讯教育平台)海外大学爬虫
    """
    name = 'qq_abroad'


    @staticmethod
    def is_chinese(word):
        for ch in word:
            if '\u4e00' <= ch <= '\u9fff':
                return False
        return True

    def __init__(self, *args, **kwargs):
        pass

    def start_requests(self):
        """初始请求"""
        # for i in range(0,779):
        #     url = 'http://uin.qq.com/index.php?r=JsonpGenerater&a=search&jsonpCallback=success_jsonpCallback&qualification_list=2&currentPage={}&_=1541082555541'.format(i)
        for i in range(0,1102):
            url = 'http://uin.qq.com/index.php?r=JsonpGenerater&a=search&jsonpCallback=success_jsonpCallback&currentPage={}&_=1541143372055'.format(i)
            yield scrapy.Request(url, callback=self.university_parse)
            
        
                      
    def university_parse(self, response):
        """Json解析"""
        dict_obj = json.loads(response.text[22:-1])
        results = dict_obj['results']
        for i in range(len(results)):
            item = UniversityItem()
            item['uni_list_link'] = response.url
            item['country_name'] = results[i]['cname']
            item['country_link'] = results[i]['ccode']
            item['area_name'] = results[i]['pname']
            item['native_uni_name'] = results[i]['ename']

            if len(results[i]['ename'].split('Now:')) > 1:
                item['english_uni_name'] = results[i]['ename'].split('Now:')[-1].split(')')[0].strip()
                if '(' in item['english_uni_name']:
                    item['english_uni_name'] = item['english_uni_name'].split('(')[0].strip()
            else:
                item['english_uni_name'] = results[i]['ename'].split('(')[0].strip()

            if len(results[i]['name'].split('现名：')) > 1:
                item['chinese_uni_name'] = results[i]['name'].split('现名：')[-1].split(')')[0].strip()
                if '(' in item['chinese_uni_name']:
                    item['chinese_uni_name'] = item['chinese_uni_name'].split('(')[0].strip()
            else:
                item['chinese_uni_name'] = results[i]['name'].split('(')[0].strip()
                        
            item['campus'] = results[i]['name']
            item['website'] = results[i]['website']
            item['last_update_date'] = datetime.now()
            yield item
        


        
