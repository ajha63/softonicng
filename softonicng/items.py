# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SoftonicngItem(scrapy.Item):
	# define the fields for your item here like:
	# name = scrapy.Field()
	title = scrapy.Field()
	os = scrapy.Field()
	description = scrapy.Field()
	image_urls = scrapy.Field()
	images = scrapy.Field()

class DownloadngItem(scrapy.Item):
	title = scrapy.Field()
	os = scrapy.Field()
	description = scrapy.Field()
	urlpack = scrapy.Field()
	image_urls = scrapy.Field()
	images = scrapy.Field()

class FileItem(scrapy.Item):
	file_urls = scrapy.Field()
	files = scrapy.Field()