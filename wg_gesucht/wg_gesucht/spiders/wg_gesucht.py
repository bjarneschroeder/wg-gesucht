import logging

from scrapy import Request, Spider


class WgGesuchtSpider(Spider):
    name = "wg_gesucht"

    def start_requests(self):
        yield Request(url="https://www.wg-gesucht.de/", callback=self.parse)

    def parse(self, response):
        logging.info(f"Got response with status {response.status}")
