# -*- coding: utf-8 -*-
import scrapy
import pprint
from softonicng.items import SoftonicngItem
from softonicng.items import FileItem


class WindsoftSpider(scrapy.Spider):
    name = 'windsoft'
    allowed_domains = ['download.cnet.com']
    start_urls = ['http://download.cnet.com/most-popular/windows/']
    def parse(self, response):
    	IND = 1
    	for item in response.xpath('//li[@class=$val]', val='list-program-item js-listed-program'):
    		strpath = '//*[@id="program_list"]/li[{:d}]/a/@href'.format(IND)
    		path = item.xpath(strpath).extract_first()
    		# yield scrapy.Request(path + '/download', callback = self.parse_download)
    		yield scrapy.Request(path, callback = self.parse_deatils)
    		IND += 1

    	next_page = response.css('a.pagination-next ::attr(href)').extract_first()
    	if next_page:
    		yield scrapy.Request(response.urljoin(next_page), callback=self.parse)

    def parse_deatils(self, response):
    	name = response.xpath('//h1[@class=$val]/text()', val='media-app__title').extract_first()
    	vers = response.xpath('//h1[@class=$val]/span/text()', val='media-app__title').extract_first()
    	try:
    		parse_title = repr('{:s} {:s}'.format(name, vers))
    	except:
    		parse_title = repr('{:s}'.format(name))

    	description = response.xpath('normalize-space(.//*[@id="app-softonic-review"]/article)').extract_first()
    	if description:
    		parse_description = repr(description)
    	else:
    		parse_description = repr("Not description")

    	os = response.xpath('normalize-space(.//p[@itemprop=$val]/text())', val='operatingSystem').extract_first()
    	if os:
    		parse_os = repr(os)
    	else:
    		parse_os = repr("Windows")

    	screenshots = response.xpath('//a[@class=$val]/@href', val='gallery__media-links').extract()

    	yield SoftonicngItem(
    		title = parse_title,
    		os = parse_os,
    		description = parse_description,
    		image_urls = screenshots,
    	)

    def parse_download(self, response):
    	pathto = '//*[@id="js-app-download-info"]/a/@href'
    	valto = 'btn btn--alternative btn--small js-alternative-button' 
    	downfile = response.xpath(pathto, val=valto).extract()
    	
    	if downfile:
    		yield FileItem(
    			file_urls = downfile
    		)
    	else:
    		self.logger.debug('[>> NOT URL to download <<]')
