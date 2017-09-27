# -*- coding: utf-8 -*-
import scrapy
import pprint
from softonicng.items import DownloadngItem


class WindsoftSpider(scrapy.Spider):
	name = 'cnetwind'
	allowed_domains = ['download.cnet.com']
	start_urls = ['http://download.cnet.com/most-popular/windows/']
	def parse(self, response):
		IND = 1
		for item in response.xpath('//*[@id="search-results"]/a'):
			pathToDetails = '//*[@id="search-results"]/a[{:d}]/@href'.format(IND)
			itemDetails = item.xpath(pathToDetails).extract_first()
			IND += 1
			yield scrapy.Request(itemDetails, callback = self.parse_package)

		next_page = response.css('a.next ::attr(href)').extract_first()
		if next_page:
			yield scrapy.Request(response.urljoin(next_page), callback=self.parse)

	def parse_package(self, response):
		img = response.xpath('//*[@id="content-body-product-single"]/header/h1/span[1]/img/@src')
		imageURL = [img.extract_first()]
		screenShots = '//*[@id="product-screenshots"]/div[2]/div/ul/li'
		for image in response.xpath(screenShots):
			imageSrc = image.css('img.om-image-view  ::attr(data-large-img)').extract_first()
			imageURL.append(imageSrc)

		yield DownloadngItem(
			image_urls = imageURL
		)