# -*- coding: utf-8 -*-
from __future__ import print_function
from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from jpy_currency.utility import Utility
from jpy_currency.spiders.currencyChina import CurrencyChinaSpider
from jpy_currency.spiders.currencyTaiwan import CurrencyTaiwanSpider
from jpy_currency.spiders.currencyFirst import CurrencyFirstSpider

spiders = [CurrencyChinaSpider, CurrencyTaiwanSpider, CurrencyFirstSpider]
sleep_interval = 30

def crawl_job():
    settings = get_project_settings()
    runner = CrawlerRunner(settings)
    for spider in spiders:
        print('spider crawl')
        runner.crawl(spider)
    return runner.join()

def after_crawl(null):
    Utility.sendMailToUser()
    reactor.callLater(sleep_interval, crawl)

def error_handle(e):
    print(e)
    Utility.destruct()

def crawl():
    d = crawl_job()
    d.addCallback(after_crawl)
    d.addErrback(error_handle)


if __name__=="__main__":
    Utility.init()
    i = 0
    #while (Utility.getDB() is None):
    #    i = i + 1
    crawl()
    reactor.run()
