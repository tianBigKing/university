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
    (新浪教育平台)海外大学爬虫
    """
    name = 'sina_abroad'


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
        for i in range(1,743):
            url = 'http://kaoshi.edu.sina.com.cn/abroad/list.php?country=&type=&zhinanflag=&collegename=&page={}'.format(i)
            yield scrapy.Request(url, callback=self.list_parse)
        
              
    def list_parse(self, response):
        """列表解析"""
        print('--------列表解析----------')
        item = UniversityItem()
        # with open('text.txt','w',encoding='utf-8') as f:
        #     f.write(response.text)
        # return 0
        uni_tr = response.xpath('//table[@class="ju1"]/tr/td[2]/table[3]//tr')
        for i in range(1, len(uni_tr)):
            item['country_link'] = response.url
            item['uni_list_link'] = uni_tr[i].xpath('./td[1]/a[1]/@href').extract()[0].strip()
            item['chinese_uni_name'] = uni_tr[i].xpath('./td[1]//text()').extract()[0].strip()
            item['country_name'] = uni_tr[i].xpath('./td[2]//text()').extract()[0].strip()
            item['nature'] = uni_tr[i].xpath('./td[4]//text()').extract()[0].strip()
            yield scrapy.Request(item['uni_list_link'], callback=self.university_parse, meta=item)
    
    def university_parse(self, response):
        print('--------英文校名解析----------')
        # english_uni_name = response.xpath('/html/body/table/tr/td[1]/table[2]/tr/td/table/tr/td[2]').extract()[0]
        pattern = r'<br />(.*?)</td>'   
        res = re.findall(pattern, response.text, re.S)
        try:
            response.meta['english_uni_name'] = res[0].split('&nbsp;')[-1].strip()
        except Exception as e:
            response.meta['english_uni_name'] = ''
        response.meta['last_update_date'] = datetime.now()
        yield response.meta


        
