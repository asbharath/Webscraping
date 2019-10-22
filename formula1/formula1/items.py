# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class Formula1Item(scrapy.Item):
    # define the fields for your item here like:

    # title_heading = scrapy.Field()
    # table_heading = scrapy.Field()
    grand_prix = scrapy.Field()
    race_date = scrapy.Field()
    winner = scrapy.Field()
    constructor = scrapy.Field()
    no_of_laps = scrapy.Field()
    time_taken = scrapy.Field()


