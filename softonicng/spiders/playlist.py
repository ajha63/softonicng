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
		# fecth images
		img = response.xpath('//*[@id="content-body-product-single"]/header/h1/span[1]/img/@src')
		imageURL = [img.extract_first()]
		screenShots = '//*[@id="product-screenshots"]/div[2]/div/ul/li'
		for image in response.xpath(screenShots):
			imageSrc = image.css('img.om-image-view  ::attr(data-large-img)').extract_first()
			imageURL.append(imageSrc)

		# fecth data
		packageNamePath = '//*[@id="content-body-product-single"]/header/h1/span[2]/text()'
		packageName = response.xpath(packageNamePath).extract_first()

		packageVerPath = '//*[@id="specsPubVersion"]/td[2]/text()'
		packageVer = response.xpath(packageVerPath).extract_first()

		osPath = '//*[@id="specsOperatingSystem"]/td[2]/text()'
		osName = response.xpath(osPath).extract_first()

		publisherDescriptionPath = 'normalize-space(//*[@id="publisher-description"]/p/text())'
		publisherDescription = response.xpath(publisherDescriptionPath).extract_first()

		editorReviewPath = 'normalize-space(//*[@id="review"]/div[2]/div/span/p[1]/text())'
		editorReview = response.xpath(editorReviewPath).extract_first()

		if publisherDescription:
			descripCaption = publisherDescription
		else:
			descripCaption = editorReview

		yield DownloadngItem(
			title = '{:s} {:s}'.format(packageName, packageVer),
			os = osName.strip(),
			description = descripCaption,
			urlpack = '{:s}'.format(response.url),
			image_urls = imageURL
		)
		logMessage = '{:s} {:s} Pulled!'.format(packageName, packageVer)
		self.logger.debug(logMessage)