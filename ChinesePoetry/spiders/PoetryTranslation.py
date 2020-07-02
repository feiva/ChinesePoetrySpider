# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ChinesePoetry.items import PoetryItemLoader, PoetryTranslationItem

class PoetrytranslationSpider(CrawlSpider):
    name = 'PoetryTranslation'
    allowed_domains = ['so.gushiwen.cn']
    start_urls = ['https://www.gushiwen.cn/']

    rules = (
        Rule(LinkExtractor(allow=r'/shiwenv_\S+.aspx$'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'/shiwen/'), follow=True),
    )

    def parse_item(self, response):
        itemloader = PoetryItemLoader(item=PoetryTranslationItem(),response=response)
        itemloader.add_value('url', response.url)
        itemloader.add_xpath('title', '//*[@class="sons"][1]/div[1]/h1/text()')
        itemloader.add_xpath('dynasty', '//*[@class="sons"][1]/div[1]/p/a[1]/text()')
        itemloader.add_xpath('author', '//*[@class="sons"][1]/div[1]/p/a[2]/text()')
        content = response.xpath('//*[@class="sons"][1]/div[1]/div[2]/text()').extract()
        if len([x for x in content if len(x.strip()) != 0]) == 0:
            content = response.xpath('//*[@class="sons"][1]/div[1]/div[2]/p/text()').extract()
        itemloader.add_value('content', content)
        itemloader.add_xpath('translation', '//*[@class="sons"][2]/div[@class="contyishang"]/p[1]/text()')
        return itemloader.load_item()
