# -*- coding: utf-8 -*-
import scrapy
import pprint
from softonicng.items import DownloadngItem
from softonicng.items import FileItem


class WindsoftSpider(scrapy.Spider):
    name = 'cnetwind'
    allowed_domains = ['download.cnet.com']
    start_urls = ['http://download.cnet.com/most-popular/windows/']
    def parse(self, response):
    	IND = 1
    	for item in response.xpath('//*[@id="search-results"]/a'):
    		pathToDetails = '//*[@id="search-results"]/a[{:d}]/@href'.format(IND)
    		itemDetails = item.xpath(pathToDetails).extract_first()
    		# remove all self.logger.debug
    		self.logger.debug(itemDetails)
    		IND += 1

    	next_page = response.css('a.next ::attr(href)').extract_first()
    	if next_page:
    		yield scrapy.Request(response.urljoin(next_page), callback=self.parse)

    def parse_package(self, response):
    	pass