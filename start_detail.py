# -*- coding: utf-8 -*-

from scrapy.cmdline import execute

def start():
    execute('scrapy crawl detail'.split())

start()