# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class DepartmentItem(scrapy.Item):
    # define the fields for your item here like:
    department = scrapy.Field()
    name = scrapy.Field()
    tel = scrapy.Field()
    fax = scrapy.Field()
    address = scrapy.Field()
    email = scrapy.Field()
    homepage = scrapy.Field()
    
