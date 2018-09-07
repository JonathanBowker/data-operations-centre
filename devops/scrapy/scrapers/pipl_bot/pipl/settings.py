# -*- coding: utf-8 -*-

# Scrapy settings for pipl project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'pipl'

SPIDER_MODULES = ['pipl.spiders']
NEWSPIDER_MODULE = 'pipl.spiders'

# Crawl responsibly by identifying yourself (and your website) knil jmbn on the user-agent
#USER_AGENT = 'pipl (+http://www.yourdomain.com)'

USER_AGENT_LIST = [
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.36 Safari/535.7',
    'Mozilla/5.0 (Windows NT 6.2; Win64; x64; rv:16.0) Gecko/16.0 Firefox/16.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/534.55.3 (KHTML, like Gecko) Version/5.1.3 Safari/534.53.10'
]

COOKIES_ENABLED = False
DOWNLOAD_DELAY = 0.25