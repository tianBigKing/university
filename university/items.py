# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy



class UniversityItem(scrapy.Item):
    # define the fields for your item here like:
    country_name = scrapy.Field()
    country_link = scrapy.Field()
    area_name = scrapy.Field()
    nature = scrapy.Field()
    uni_list_link = scrapy.Field()
    campus = scrapy.Field()
    native_uni_name = scrapy.Field()
    chinese_uni_name = scrapy.Field()
    english_uni_name = scrapy.Field()
    website = scrapy.Field()
    remarks = scrapy.Field()
    last_update_date = scrapy.Field(serializer=str)
    

class AreaItem(scrapy.Item):
    country = scrapy.Field()
    code = scrapy.Field()
    provice = scrapy.Field()
    city = scrapy.Field()
    remarks = scrapy.Field()
    last_update_date = scrapy.Field(serializer=str)

