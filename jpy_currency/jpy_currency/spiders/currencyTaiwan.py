# -*- coding: utf-8 -*-
import scrapy
import re
from datetime import datetime
from jpy_currency.items import CurrencyItem

class CurrencyTaiwanSpider(scrapy.Spider):
    name = 'currencyTaiwan'

    def start_requests(self):
        print('start crawl Taiwan bank')
        urls = ['https://rate.bot.com.tw/xrt?Lang=zh-TW']
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        print('response:%s' % response)
        item = CurrencyItem(
            name = 'Taiwan bank',
            updated_time = datetime.now()
        )
        currency_table = response.xpath(
          '//div[1]/main/div[4]/table/tbody'
        )
        jpy = ''
        for row in currency_table.xpath('tr'):
            currencies= []
            for col in row.xpath('td'):
                country_block = col.xpath('div')
                if not country_block.extract_first() is None:
                    country = country_block.xpath(
                        'div[@class="visible-phone print_hide"]/text()[normalize-space()]'
                    ).extract_first("")
                    currencies.append(country)
                    continue
                c = col.xpath('text()').extract_first("0")
                currencies.append(c)
            if re.match('\W*JPY\W*', currencies[0]):
                jpy = currencies[2]
        item['jpy'] = jpy
        yield item

