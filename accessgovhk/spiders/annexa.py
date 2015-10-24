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
            item['name'] = str.join("", Selector(text = departmentinfo[0]).xpath('//text()').extract()).strip()
            item['tel'] = str.join("", Selector(text = departmentinfo[1]).xpath('//text()').extract()).strip()
            item['fax'] = str.join("", Selector(text = departmentinfo[2]).xpath('//text()').extract()).strip()
            item['address'] = str.join("\n", Selector(text = departmentinfo[3]).xpath('//text()').extract()).strip()
            item['homepage'] = homepage
            yield item
        else:
            tablexpaths = response.xpath('//body/table[count(tr)=4]')
            for idtable, tablexpath in enumerate(tablexpaths):
                item = DepartmentItem()
                if "police" in homepage:
                    subdep = str.join("", Selector(text = tablexpath.xpath('preceding-sibling::*[2]').extract()[0]).xpath('//text()').extract()).strip()
                else:
                    subdep = str.join("", Selector(text = tablexpath.xpath('preceding-sibling::*[1]').extract()[0]).xpath('//text()').extract()).strip()
                item['department'] = response.meta['department']
                item['subdepartment'] = subdep
                subdepartmentinfo = tablexpath.xpath('tr/*[2]').extract()
                print "subdepartmentinfo: ", subdepartmentinfo
                item['name'] = str.join("", Selector(text = subdepartmentinfo[0]).xpath('//text()').extract()).strip()
                item['tel'] = str.join("", Selector(text = subdepartmentinfo[1]).xpath('//text()').extract()).strip()
                item['fax'] = str.join("", Selector(text = subdepartmentinfo[2]).xpath('//text()').extract()).strip()
                item['address'] = str.join("\n", Selector(text = subdepartmentinfo[3]).xpath('//text()').extract()).strip()
                item['homepage'] = homepage
                yield item
