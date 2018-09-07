from __future__ import absolute_import

from scrapy import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Identity
from scrapy.spiders import Rule

from ..utils.spiders import BasePortiaSpider
from ..utils.starturls import FeedGenerator, FragmentGenerator
from ..utils.processors import Item, Field, Text, Number, Price, Date, Url, Image, Regex
from ..items import PortiaItem


class DocumentsAcerRemitEu(BasePortiaSpider):
    name = "documents.acer-remit.eu"
    allowed_domains = [u'documents.acer-remit.eu']
    start_urls = [u'https://documents.acer-remit.eu/category/all-documents/']
    rules = [
        Rule(
            LinkExtractor(
                allow=('.*'),
                deny=()
            ),
            callback='parse_item',
            follow=True
        )
    ]
    items = [[Item(PortiaItem,
                   None,
                   u'fieldset',
                   [Field(u'Title',
                          '.category-remit-and-implementing-regulation > legend *::text',
                          []),
                       Field(u'Description',
                             '.page > p *::text',
                             []),
                       Field(u'DocumentURL',
                             '.post-913 > p:nth-child(3) > strong > a::attr(href)',
                             []),
                       Field(u'LastUpdate',
                             '.post-913 > p:nth-child(4) > span *::text',
                             [Date()]),
                       Field(u'field1',
                             '.post-1523 > ul:nth-child(10) > li *::text',
                             [])])]]
