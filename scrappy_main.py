from scrapy.crawler import CrawlerProcess
from bookscrapper.bookscrapper.spiders.categorycrapper import CategorycrapperSpider

process = CrawlerProcess()
process.crawl(CategorycrapperSpider)
process.start()
