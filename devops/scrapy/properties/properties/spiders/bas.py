# -*- coding: utf-8 -*-
import scrapy


class BasSpider(scrapy.Spider):
    name = "bas"
    allowed_domains = ["web"]
    start_urls = ['http://web/']

    def parse(self, response):
        pass
