# coding=utf-8
import re
import json
import time
from datetime import datetime
from lxml import etree
import scrapy
from university.items import AreaItem
from scrapy.conf import settings


class University(scrapy.Spider):
    """
    地区、区号爬虫
    """
    name = 'area'


    def __init__(self, *args, **kwargs):
        pass

    def start_requests(self):
        """初始请求"""
        # url = 'http://4.url.cn/zc/chs/js/10062/location_chs.js'
        # url = 'http://www.51zzl.com/rcsh/gjqh.asp'
        url = 'https://www.baidu.com/'
        yield scrapy.Request(url, callback=self.area_parse)
       
            
    def code_parse(self, response):
        l = []
        tr_list = response.xpath('//*[@id="content"]/table/tbody/tr')
        for tr in tr_list:
            if tr_list.index(tr) == 0:
                continue
            item = {}
            item['country_name'] = tr.xpath('./td[2]/text()').extract()[0].strip()
            item['code'] = tr.xpath('./td[4]/text()').extract()[0].strip()
            l.append(item)
        path = 'code.json'
        self.save2json(path, {'codeList':l})
                           
    def area_parse(self, response):
        """Json解析"""
        # data_str = response.text[13:-3]
        # dict_obj = json.loads(response.text[13:-3])
        # self.save2json(path, data_str)
        item = AreaItem()
        path = 'areaOftheWorld.json'
        code_path = 'code.json'
        
        data_dict = self.read2json(path)
        code_list = self.read2json(code_path)['codeList']

        country_list = data_dict['Location']['CountryRegion']
        for country_dict in country_list:
            # if country_dict['-Name'] == '中国':
            #     continue
            #去掉没有行政区的地区
            if not country_dict.get('State'):
                continue

            item['country'] = country_dict['-Name']
            item['provice'] = ''

            #电话区号
            for code_dict in code_list:
                if code_dict['country_name'] == country_dict['-Name']:
                    item['code'] = '+' + code_dict['code']
                    break

            #根据数据类型判断行政区级别
            if isinstance(country_dict['State'],dict):
                for city_dict in country_dict['State']['City']:
                    item['city'] = city_dict['-Name']
                    item['last_update_date'] = datetime.now()
                    yield item                  
            else:
                for state_dict in country_dict['State']:
                    item['provice'] = state_dict['-Name']
                    if not state_dict.get('City'):
                        yield item
                        continue
                    if isinstance(state_dict['City'],dict):
                        item['city'] = state_dict['City']['-Name']
                        item['last_update_date'] = datetime.now()
                        yield item                  
                    else:
                        for city_dict in state_dict['City']:
                            item['city'] = city_dict['-Name']
                            item['last_update_date'] = datetime.now()
                            yield item
                            

            

    def save2json(self, path, data):
        with open(path, 'w', encoding='utf-8') as fw:
            json.dump(data, fw, ensure_ascii=False)

    def read2json(self, path):
        data_dict = ''
        with open(path, 'r', encoding='utf-8') as fr:
            data_dict = json.load(fr)
        return data_dict


        
