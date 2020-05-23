# -*- coding: utf-8 -*-

import logging
import scrapy
from ChinesePoetry.items import PoetryItemLoader, TangPoetryItem

class TangpoetrySpider(scrapy.Spider):
    name = 'TangPoetry'
    allowed_domains = ['www16.zzu.edu.cn']
    start_urls = ['http://www16.zzu.edu.cn/qtss/zzjpoem1.dll/query']
    # 43087 条

    def parse(self, response):
        href_list = response.xpath('//a/@href').extract()[2:]
        page_list = response.xpath('//div[1]/center/table/tr[2]/td/table/*/*/font/text()').extract()
        for href, page in zip(href_list,page_list):
            yield scrapy.Request(url=href, meta={"page": page}, callback=self.parse_page)

    def parse_page(self, response):
        page = response.meta.get("page","null")
        next = response.xpath('//div[1]/center/table/tr[2]/td[2]/p/a[contains(text(), "下页")]/@href')
        # count = response.xpath('//div[1]/center/table/tr[2]/td[2]/p/font[1]/text()').extract_first()
        # logging.warning(count)
        poetry_list = response.xpath('//div[1]/center/table/tr[3]/td/table/tr')[1:]

        for poetry in poetry_list:
            pageId = poetry.xpath('td[2]/font/text()').extract_first()
            pageNumber = poetry.xpath('td[3]/font/text()').extract_first()
            url = poetry.xpath('td[4]/span/a/@href').extract_first()
            yield scrapy.Request(url=url, meta={"page":page, "pageId": pageId, "pageNumber":pageNumber}, callback=self.parse_poetry)
        if next:
            yield scrapy.Request(url=next.extract_first(), meta={"page": page}, callback=self.parse_page)

    def parse_poetry(self, response):
        itemloader = PoetryItemLoader(item=TangPoetryItem(),response=response)
        itemloader.add_value('id', '')
        itemloader.add_value('pid', '')
        itemloader.add_xpath('title', '//div[1]/center/table/tr[3]/td/p/font/text()')
        author = response.xpath('//div[1]/center/table/tr[4]/td/p/a/font/u/text()').extract_first()
        if not author:
            author = '佚名'
        itemloader.add_value('author', author)
        itemloader.add_value('page', response.meta.get("page", ''))
        itemloader.add_value('pageId', response.meta.get("pageId", ''))
        itemloader.add_value('pageNumber', response.meta.get("pageNumber", ''))
        itemloader.add_value('dynasty', '唐朝')
        itemloader.add_value('lang', '简体中文')
        itemloader.add_xpath('content', '//div[1]/center/table/tr[5]/td/p/font/text()')

        itemloader.add_value('hour', '')
        itemloader.add_value('season', '')
        itemloader.add_value('weather', '')
        itemloader.add_value('location', '')
        itemloader.add_value('sentiment', '')
        itemloader.add_value('type', '')
        itemloader.add_value('character', '')

        itemloader.add_value('fromBy', '全唐诗库')
        itemloader.add_value('url', response.url)

        return itemloader.load_item()