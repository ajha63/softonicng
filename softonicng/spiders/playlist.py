# -*- coding: utf-8 -*-
import scrapy
import pprint
from softonicng.items import SoftonicngItem
from softonicng.items import FileItem


class WindsoftSpider(scrapy.Spider):
    name = 'cnetwind'
    allowed_domains = ['download.cnet.com']
    start_urls = ['http://download.cnet.com/most-popular/windows/']
    def parse(self, response):
    	IND = 1
    	for item in response.xpath('//*[@id="search-results"]/a'):
    		topath = '//*[@id="search-results"]/a[{:d}]/@href'.format(IND)
    		item.xpath(topath).extract_first()
    		IND += 1

    	next_page = response.css('a.next ::attr(href)').extract_first()
    	if next_page:
    		yield scrapy.Request(response.urljoin(next_page), callback=self.parse)