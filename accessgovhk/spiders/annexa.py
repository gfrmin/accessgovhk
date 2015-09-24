# -*- coding: utf-8 -*-
import scrapy

from accessgovhk.items import DepartmentItem
from scrapy.selector import Selector

class AnnexaSpider(scrapy.Spider):
    name = "annexa"
    allowed_domains = ["access.gov.hk"]
    start_urls = [
        'http://www.access.gov.hk/en/code.htm'
    ]

    def parse(self, response):
        departments = response.xpath('//blockquote/p/a')
        departmentnames = departments.xpath('span/text()').extract()
        departmentlinks = departments.xpath('@href').extract()
        for idhref, href in enumerate(departmentlinks):
            url = response.urljoin(href)
            request = scrapy.Request(url, callback=self.parsedeptpage)
            request.meta['department'] = departmentnames[idhref]
            yield request

    def parsedeptpage(self, response):
        homepage = response.css("a::attr(href)")[-1].extract()
        if len(response.css("table")) == 1:
            item = DepartmentItem()
            item['department'] = response.meta['department']
            departmentinfo = response.xpath('//tr/*[2]').extract()
            item['name'] = departmentinfo[0]
            item['tel'] = departmentinfo[1]
            item['fax'] = departmentinfo[2]
            item['address'] = departmentinfo[3]
            item['homepage'] = homepage
            yield item
        else:
            tablexpaths = response.xpath('//body/table[count(tr)=4]')
            for idtable, tablexpath in enumerate(tablexpaths):
                item = DepartmentItem()
                subdep = str.join("", Selector(text = tablexpath.xpath('preceding-sibling::*[1]').extract()[0]).xpath('//text()').extract()).strip()
                item['department'] = response.meta['department']
                item['subdepartment'] = subdep
                subdepartmentinfo = tablexpath.xpath('tr/*[2]').extract()
                print "subdepartmentinfo: ", subdepartmentinfo
                item['name'] = subdepartmentinfo[0]
                item['tel'] = subdepartmentinfo[1]
                item['fax'] = subdepartmentinfo[2]
                item['address'] = subdepartmentinfo[3]
                item['homepage'] = homepage
                yield item
