# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql


class UniversityPipeline(object):
    insertSql = '''insert into  sina_abroad(
    country_name,
    country_link,
    area_name,
    uni_list_link,
    native_uni_name,
    campus,
    chinese_uni_name,
    website,
    remarks,
    english_uni_name,
    nature,
    last_update_date
    )
    values(
    '{country_name}',
    '{country_link}',
    '{area_name}',
    '{uni_list_link}',
    '{native_uni_name}',
    '{campus}',
    '{chinese_uni_name}',
    '{website}',
    '{remarks}',
    '{english_uni_name}',
    '{nature}',
    '{last_update_date}'
    )'''
  

    def __init__(self, settings):
        self.connect = pymysql.connect(
             host='localhost',
             port=3306,
             user='test',  
             passwd='123456',  
             db='university',  
             charset='utf8'   
)

    def process_item(self, item, spider):
        sqltext = self.insertSql.format(
                country_name=item.get('country_name'),
                country_link=item.get('country_link'),
                area_name=item.get('area_name'),
                uni_list_link=item.get('uni_list_link'),
                native_uni_name=item.get('native_uni_name'),
                campus=item.get('campus'),
                chinese_uni_name=item.get('chinese_uni_name'),
                website=item.get('website'),
                remarks=item.get('remarks'),
                english_uni_name=item.get('english_uni_name'),
                nature=item.get('nature'),
                last_update_date=item.get('last_update_date')
               )
        self.cursor.execute(sqltext)
        return item

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def open_spider(self, spider):
        self.cursor = self.connect.cursor();
        self.connect.autocommit(True)

    def close_spider(self, spider):
        self.cursor.close()
        self.connect.close()


