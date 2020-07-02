# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import hashlib
import logging

from scrapy.exporters import CsvItemExporter, JsonItemExporter
from ChinesePoetry.items import TangPoetryItem, PoetryTranslationItem


def get_md5(string):
    if isinstance(string, str):
        string = string.encode("utf-8")
    m = hashlib.md5()
    m.update(string)
    return m.hexdigest()


class CSVPipeline:
    # FEED_EXPORT_FIELDS =

    def __init__(self):
        self.file = open('data/PoetryTranslation.csv', 'wb')
        self.exporter = CsvItemExporter(self.file, include_headers_line=True,encoding='utf-8')
        self.exporter.fields_to_export = PoetryTranslationItem.KEYS
        self.exporter.start_exporting()
        self.saved_list = []

    def process_item(self, item, spider):
        if item:
            item['id'] = len(self.saved_list)
            item['pid'] = get_md5(item['author']+item['title'])
            # item['pid'] = pid + '_' + item['pageId'][1:-1] + '_' + item['pageNumber'][1:-1]
            # item['pid'] = get_md5(item['author']+item['title']+item['pageId'][1:-1]+item['pageNumber'][1:-1])
            if item['pid'] not in self.saved_list:
                self.exporter.export_item(item)
                self.saved_list.append(item['pid'])
        if len(self.saved_list) % 100 == 0:
            print('saved csv size: %s' % len(self.saved_list))
            logging.info('saved size: %s' % len(self.saved_list))
        return item

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()
        logging.info('Saved csv item size: {0}'.format(len(self.saved_list)))


class JsonPipeline:

    def __init__(self):
        self.file = open('data/TangPoetry.json', 'wb')
        self.exporter = JsonItemExporter(self.file, ensure_ascii=False, encoding='utf-8')
        self.exporter.fields_to_export = TangPoetryItem.KEYS
        self.exporter.start_exporting()
        self.saved_list = []

    def process_item(self, item, spider):
        if item:
            # item['id'] = len(self.saved_list)
            # pid = get_md5(item['author']+item['title'])
            # item['pid'] = pid + '_' + item['pageId'][1:-1] + '_' + item['pageNumber'][1:-1]
            # item['pid'] = get_md5(item['author']+item['title']+item['pageId'][1:-1]+item['pageNumber'][1:-1])
            if item['pid'] not in self.saved_list:
                self.exporter.export_item(item)
                self.saved_list.append(item['pid'])
        if len(self.saved_list)%100 == 0:
            print('saved json size: %s' % len(self.saved_list))
            logging.info('saved size: %s' % len(self.saved_list))
        return item

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()
        logging.info('Saved json item size: {0}'.format(len(self.saved_list)))