# -*- coding: utf-8 -*-
import scrapy

from accessgovhk.items import DepartmentItem
from scrapy.selector import Selector
from string import whitespace

class NewAccessSpider(scrapy.Spider):
    name = "newaccess"
    allowed_domains = ["access.gov.hk"]
    start_urls = [
        'http://www.access.gov.hk/en/howtomakeinfo/index.html'
    ]

    def parse(self, response):
        departments = response.css('#content .clearfix a')
        departmentlinks = [link.strip() for link in departments.xpath('@href').extract() if link != u'javascript:void(0);'] # because there are pointless void(0) links....!?!?
        for href in departmentlinks:
            url = response.urljoin(href)
            request = scrapy.Request(url, callback=self.parsedeptpage)
            yield request

    def parsedeptpage(self, response):
        if not response.css(".btn_website"):
            return
        departmentname = " ".join(response.css("h2::text").extract_first().split())
        homepage = response.css(".btn_website::attr(href)").extract_first()
        if not response.css("h4"):
            item = DepartmentItem()
            item['department'] = departmentname
            departmentinfo = response.css('p').extract()
            item['name'] = str.join("", Selector(text = departmentinfo[0]).xpath('//text()').extract()).strip()
            item['tel'] = str.join("", Selector(text = departmentinfo[1]).xpath('//text()').extract()).strip()
            item['fax'] = str.join("", Selector(text = departmentinfo[2]).xpath('//text()').extract()).strip()
            item['email'] = str.join("", Selector(text = departmentinfo[3]).xpath('//text()').extract()).strip()
            item['address'] = ", ".join([x.strip() for x in Selector(text = departmentinfo[4]).xpath('//text()').extract()]).replace(",,", ",")
            item['homepage'] = homepage
            yield item
        else:
            departmentinfo = response.css('p').extract()
            for sectionid, subdepartmentsection in enumerate(response.css("h3::text").extract()):
                subdepartmentinfo = departmentinfo[(sectionid*5):((sectionid+1)*5)]
                item = DepartmentItem()
                item['department'] = departmentname + " " + subdepartmentsection.strip()
                item['name'] = str.join("", Selector(text = subdepartmentinfo[0]).xpath('//text()').extract()).strip()
                item['tel'] = str.join("", Selector(text = subdepartmentinfo[1]).xpath('//text()').extract()).strip()
                item['fax'] = str.join("", Selector(text = subdepartmentinfo[2]).xpath('//text()').extract()).strip()
                item['email'] = str.join("", Selector(text = subdepartmentinfo[3]).xpath('//text()').extract()).strip()
                item['address'] = ", ".join([x.strip() for x in Selector(text = subdepartmentinfo[4]).xpath('//text()').extract()]).replace(",,", ",")
                item['homepage'] = homepage
                yield item
            if response.css(".tabController"):
                tabpagelinks = response.css(".tab a::attr(href)").extract()
                for href in tabpagelinks:
                    url = response.urljoin(href)
                    request = scrapy.Request(url, callback=self.parsedeptpage)
                    yield request
