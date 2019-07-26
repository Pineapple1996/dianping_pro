# -*- coding: utf-8 -*-

from scrapy.cmdline import execute

def start():
    execute('scrapy crawl search '.split())


if __name__ == '__main__':
    start()