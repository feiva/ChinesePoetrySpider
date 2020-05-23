# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst, Join


def strip(value):
    return value.strip()


def fillna(value):
    if value is None or len(value) == 0:
        return 'null'
    return value


def process_content(value):
    return value.strip().replace('<br>', '').replace('&nbsp;','')


def process_pageId(value):
    return '第'+value+'卷'


def process_pageNumber(value):
    return '第'+value+'首'


class PoetryItemLoader(ItemLoader):
    default_output_processor = TakeFirst()
    default_input_processor = MapCompose(strip,fillna)


class TangPoetryItem(scrapy.Item):
    KEYS = [
            'id',
            'pid',
            'title',
            'author',
            'page',
            'pageId',
            'pageNumber',
            'dynasty',
            'lang',
            'content',
            # 'hour',
            # 'season',
            # 'weather',
            # 'location',
            # 'sentiment',
            # 'type',
            # 'character',
            'fromBy',
            'url'
    ]

    id = scrapy.Field()
    pid = scrapy.Field()
    title = scrapy.Field()
    author = scrapy.Field()
    page = scrapy.Field()
    pageId = scrapy.Field(
        input_processor = MapCompose(process_pageId)
    )
    pageNumber = scrapy.Field(
        input_processor = MapCompose(process_pageNumber)
    )
    dynasty = scrapy.Field()
    lang = scrapy.Field()
    content = scrapy.Field(
        input_processor = MapCompose(process_content),
        output_processor = Join()
    )
    hour = scrapy.Field()
    season = scrapy.Field()
    weather = scrapy.Field()
    location = scrapy.Field()
    sentiment = scrapy.Field()
    type = scrapy.Field()
    character = scrapy.Field()
    fromBy = scrapy.Field()
    url = scrapy.Field()

    def keys(self):
        return self.KEYS