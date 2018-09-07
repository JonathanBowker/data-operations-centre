SPIDER_MODULES = ['lechat_bot.spiders']
NEWSPIDER_MODULE = 'lechat_bot.spiders'
DOWNLOADER_MIDDLEWARES = {
    'lechat_bot.middlewares.MyMetaRefreshMiddleware': 543,
    'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware': None,
    'scrapy.contrib.downloadermiddleware.redirect.MetaRefreshMiddleware': None,
}
DOWNLOAD_DELAY = 15
REDIRECT_MAX_TIMES = 200000
USER_AGENT = "Mozilla/5.0 (Windows NT 6.1; rv:31.0) Gecko/20100101 Firefox/31.0"
