# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BookscraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
class BookItem(scrapy.Item):
    # define the fields for your item here like:
    title=scrapy.Field()
    prod_description=scrapy.Field()
    category=scrapy.Field()
    product_type=scrapy.Field()
    price_exc_tax=scrapy.Field()
    price_inc_tax=scrapy.Field()
    tax=scrapy.Field()
    availability=scrapy.Field()
    num_reviews=scrapy.Field()
    price=scrapy.Field()
    rating=scrapy.Field()