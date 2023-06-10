# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class FlatItem(scrapy.Item):
    id = scrapy.Field()
    meta = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    rooms = scrapy.Field()
    size = scrapy.Field()
    rent_costs = scrapy.Field()
    utilities_costs = scrapy.Field()
    additional_flat_costs = scrapy.Field()
    other_costs = scrapy.Field()
    deposit = scrapy.Field()
    street = scrapy.Field()
    postal_code = scrapy.Field()
    city_name = scrapy.Field()
    move_in_date = scrapy.Field()
    move_in_date_ts = scrapy.Field()
