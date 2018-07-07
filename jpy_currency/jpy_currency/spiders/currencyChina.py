# -*- coding: utf-8 -*-                                                                
import scrapy
import re
from datetime import datetime
from jpy_currency.items import CurrencyItem

class CurrencyChinaSpider(scrapy.Spider):
    name = "currencyChina"

    def start_requests(self):
        print('start request china trust')
        urls = [
            'https://www.ctbcbank.com/CTCBPortalWeb/toPage?id=TW_RB_CM_ebank_018001'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        print('china trust:%s' % response)
        item = CurrencyItem(
            name = 'china bank',
            updated_time = datetime.now()
        )
        currency_table = response.xpath(
            '//*[@id="mainTable"]'
        )
        jpy = []
        for row in currency_table.xpath('tr'):
            currencies = [col.xpath('normalize-space(text())').extract_first('0') for
                          col in row.xpath('td') ]
            if re.match('\W*JPY\W*', currencies[0]):
                jpy = currencies[2]
        item['jpy'] = jpy
        yield item
