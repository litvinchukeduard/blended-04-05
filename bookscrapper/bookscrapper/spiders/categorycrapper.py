import scrapy


class CategorycrapperSpider(scrapy.Spider):
    name = "categorycrapper"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com"]

    def parse(self, response):
        for ul in response.css('ul.nav-list'):
            for a in ul.css('a'):
                print(a.css('::text').get().strip())
                yield {'category': a.css('::text').get().strip()}
            # yield {'category' : element.css('text').get().strip()}

