 # -*- coding: utf-8 -*-

# Scrapy settings for i2p project
#
# For simplicity, this file contains only settings considered important or
# commonly used. More settings and their documentation in:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'i2p'

SPIDER_MODULES = ['i2p.spiders']
NEWSPIDER_MODULE = 'i2p.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'i2p (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 5
DOWNLOAD_TIMEOUT = 30 # 30s
RETRY_TIMES = 2
# The download delay setting will honor only one of:
CONCURRENT_REQUESTS_PER_DOMAIN = 1
CONCURRENT_REQUESTS_PER_IP = 1

# Disable cookies (enabled by default)
COOKIES_ENABLED = True

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
SPIDER_MIDDLEWARES = {
   'i2p.middlewares.I2PSpiderMiddleware': 543,
   'scrapy_splash.SplashDeduplicateArgsMiddleware': 100
}

SPLASH_URL = 'http://192.168.59.103:8050'

SELENIUM_DRIVER_NAME = 'chrome' #driver
SELENIUM_DRIVER_EXECUTABLE_PATH = '/usr/bin/chromedriver' #driver
#chrome
SELENIUM_DRIVER_ARGUMENTS=['--headless', '--no-sandbox', '--disable-gpu'] 

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'i2p.middlewares.I2PProxyMiddleware': 200,
    'i2p.middlewares.I2PFilterMiddleware': 300,
    'scrapy_selenium.SeleniumMiddleware': 800,
    'scrapy_splash.SplashCookiesMiddleware': 723,
    'scrapy_splash.SplashMiddleware': 725,
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'i2p.pipelines.I2PPipeline': 300,
#}

# The maximum depth that will be allowed to crawl for any site:
DEPTH_LIMIT = 1

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
HTTPCACHE_ENABLED = False
HTTPCACHE_EXPIRATION_SECS = 0
HTTPCACHE_DIR = 'httpcache'
HTTPCACHE_IGNORE_HTTP_CODES = []
HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
